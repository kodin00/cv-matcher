import csv
import json
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.insert(0, "/app")

from sentence_transformers import util

from services.baseline_service import compute_keyword_score
from services.embedding_service import chunk_text, get_model
from services.extraction import segment_cv
from services.preprocessing import detect_language, normalize


CV_CSV = os.getenv("CV_CSV", "/tmp/cv_texts.csv")
OUTPUT_CSV = os.getenv("OUTPUT_CSV", "/tmp/cv_job_match_results.csv")
DB_FILE = os.getenv("DB_FILE", "/app/data/app.db")


def read_cvs(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_jobs(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT id, title, company, industry, description, required_skills,
               required_experience_years, required_education
        FROM jobs
        ORDER BY rowid
        """
    ).fetchall()
    con.close()
    jobs = []
    for row in rows:
        job = dict(row)
        job["required_skills"] = json.loads(job["required_skills"])
        jobs.append(job)
    return jobs


def pool_texts(model, text_by_key):
    all_chunks = []
    spans = {}

    for key, text in text_by_key.items():
        chunks = chunk_text(text or "")
        start = len(all_chunks)
        all_chunks.extend(chunks)
        spans[key] = (start, len(all_chunks))

    if not all_chunks:
        return {key: None for key in text_by_key}

    embeddings = model.encode(
        all_chunks,
        convert_to_tensor=True,
        show_progress_bar=False,
    )

    pooled = {}
    for key, (start, end) in spans.items():
        if start == end:
            pooled[key] = None
        else:
            pooled[key] = embeddings[start:end].mean(dim=0, keepdim=True)
    return pooled


def section_score_from_pooled(left, right):
    if left is None or right is None:
        return 0.0
    similarity = util.cos_sim(left, right).item()
    return round(max(0.0, similarity) * 100.0, 2)


def rank_rows(rows, score_key, rank_key):
    by_cv = defaultdict(list)
    for row in rows:
        by_cv[row["cv_id"]].append(row)

    for cv_rows in by_cv.values():
        sorted_rows = sorted(cv_rows, key=lambda item: item[score_key], reverse=True)
        previous_score = None
        previous_rank = 0
        for index, row in enumerate(sorted_rows, start=1):
            if row[score_key] == previous_score:
                row[rank_key] = previous_rank
            else:
                row[rank_key] = index
                previous_rank = index
                previous_score = row[score_key]


def main():
    cvs = read_cvs(CV_CSV)
    jobs = read_jobs(DB_FILE)

    processed_cvs = []
    for cv in cvs:
        cleaned = normalize(cv["raw_text"])
        processed_cvs.append(
            {
                "cv_id": cv["cv_id"],
                "raw_text": cv["raw_text"],
                "cleaned": cleaned,
                "language_detected": detect_language(cleaned) or "unknown",
                "sections": segment_cv(cleaned),
            }
        )

    model = get_model()

    cv_skill_embeddings = pool_texts(
        model,
        {cv["cv_id"]: cv["sections"]["skills"] for cv in processed_cvs},
    )
    cv_experience_embeddings = pool_texts(
        model,
        {cv["cv_id"]: cv["sections"]["experience"] for cv in processed_cvs},
    )
    cv_education_embeddings = pool_texts(
        model,
        {cv["cv_id"]: cv["sections"]["education"] for cv in processed_cvs},
    )
    job_skill_embeddings = pool_texts(
        model,
        {job["id"]: " ".join(job["required_skills"]) for job in jobs},
    )
    job_description_embeddings = pool_texts(
        model,
        {job["id"]: job["description"] for job in jobs},
    )
    job_education_embeddings = pool_texts(
        model,
        {job["id"]: job["required_education"] or "" for job in jobs},
    )

    rows = []
    total = len(processed_cvs) * len(jobs)
    done = 0

    for cv in processed_cvs:
        for job in jobs:
            skills_score = section_score_from_pooled(
                cv_skill_embeddings[cv["cv_id"]],
                job_skill_embeddings[job["id"]],
            )
            experience_score = section_score_from_pooled(
                cv_experience_embeddings[cv["cv_id"]],
                job_description_embeddings[job["id"]],
            )
            education_score = section_score_from_pooled(
                cv_education_embeddings[cv["cv_id"]],
                job_education_embeddings[job["id"]],
            )
            semantic_score = round(
                (skills_score * 0.4) + (experience_score * 0.4) + (education_score * 0.2),
                2,
            )
            jd_full_text = job["description"] + " " + " ".join(job["required_skills"])
            keyword_score = float(compute_keyword_score(cv["raw_text"], jd_full_text))

            rows.append(
                {
                    "cv_id": cv["cv_id"],
                    "job_id": job["id"],
                    "job_title": job["title"],
                    "company": job["company"],
                    "industry": job["industry"],
                    "language_detected": cv["language_detected"],
                    "required_experience_years": job["required_experience_years"],
                    "required_education": job["required_education"],
                    "semantic_score_percent": semantic_score,
                    "keyword_score_percent": keyword_score,
                    "improvement_percent": round(semantic_score - keyword_score, 2),
                    "semantic_skills_score_percent": skills_score,
                    "semantic_experience_score_percent": experience_score,
                    "semantic_education_score_percent": education_score,
                }
            )
            done += 1
            if done % 250 == 0:
                print(f"processed {done}/{total}", flush=True)

    rank_rows(rows, "semantic_score_percent", "semantic_rank_for_cv")
    rank_rows(rows, "keyword_score_percent", "keyword_rank_for_cv")

    fieldnames = [
        "cv_id",
        "job_id",
        "job_title",
        "company",
        "industry",
        "language_detected",
        "required_experience_years",
        "required_education",
        "semantic_score_percent",
        "keyword_score_percent",
        "improvement_percent",
        "semantic_rank_for_cv",
        "keyword_rank_for_cv",
        "semantic_skills_score_percent",
        "semantic_experience_score_percent",
        "semantic_education_score_percent",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {OUTPUT_CSV}", flush=True)


if __name__ == "__main__":
    main()
