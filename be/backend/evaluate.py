"""
Standalone evaluation script for the CV semantic matching pipeline.

Usage:
    python evaluate.py --dataset data/eval_pairs.csv

The dataset file must have columns: cv_text, job_id, label
  label: 1 = Relevant, 0 = Not Relevant

Outputs Precision, Recall, and F1-Score for both the semantic (sentence-transformers)
and TF-IDF baseline methods side by side.

Threshold: score >= 60 → predicted Relevant (1), else Not Relevant (0)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys

# Allow imports from the backend directory when running directly
sys.path.insert(0, os.path.dirname(__file__))

from models.db_models import get_db, Job
from services.preprocessing import normalize, detect_language
from services.extraction import segment_cv, extract_skills
from services.embedding_service import compute_match
from services.baseline_service import compute_keyword_score

THRESHOLD = 60.0


def _load_dataset(path: str) -> list[dict]:
    ext = os.path.splitext(path)[1].lower()
    rows = []
    if ext == ".json":
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
    else:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "cv_text": row["cv_text"],
                    "job_id":  row["job_id"],
                    "label":   int(row["label"]),
                })
    return rows


def _fetch_job(db, job_id: str) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()


def _build_jd_dict(job: Job) -> dict:
    return {
        "required_skills":          job.skills_list(),
        "description":              job.description,
        "required_education":       job.required_education or "",
        "required_experience_years": job.required_experience_years,
    }


def _precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) > 0 else 0.0)
    return round(precision, 4), round(recall, 4), round(f1, 4)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate semantic vs TF-IDF matching.")
    parser.add_argument("--dataset", required=True, help="Path to labeled dataset (CSV or JSON)")
    args = parser.parse_args()

    rows = _load_dataset(args.dataset)
    total = len(rows)
    print(f"Loaded {total} evaluation pairs from '{args.dataset}'")

    db = get_db()

    # Confusion matrix counters: [semantic, tfidf]
    tp = [0, 0]
    fp = [0, 0]
    fn = [0, 0]
    tn = [0, 0]

    skipped = 0
    for i, row in enumerate(rows, start=1):
        job_id  = row["job_id"]
        cv_text = row["cv_text"]
        label   = row["label"]

        job = _fetch_job(db, job_id)
        if job is None:
            print(f"  [WARN] Row {i}: job_id '{job_id}' not found — skipping.")
            skipped += 1
            continue

        jd_dict    = _build_jd_dict(job)
        jd_full    = job.description + " " + " ".join(job.skills_list())

        cleaned    = normalize(cv_text)
        cv_sections = segment_cv(cleaned)

        scores          = compute_match(cv_sections, jd_dict)
        semantic_score  = scores["semantic_score"]

        keyword_score   = compute_keyword_score(cleaned, jd_full)

        for idx, score in enumerate([semantic_score, keyword_score]):
            predicted = 1 if score >= THRESHOLD else 0
            if predicted == 1 and label == 1:
                tp[idx] += 1
            elif predicted == 1 and label == 0:
                fp[idx] += 1
            elif predicted == 0 and label == 1:
                fn[idx] += 1
            else:
                tn[idx] += 1

        if i % 50 == 0:
            print(f"  Processed {i}/{total}...")

    db.close()

    evaluated = total - skipped
    print(f"\nEvaluated {evaluated} pairs ({skipped} skipped).\n")
    print(f"Threshold: score >= {THRESHOLD:.0f} → Relevant\n")

    headers = ["Method", "Precision", "Recall", "F1-Score", "TP", "FP", "FN", "TN"]
    row_fmt = "{:<22} {:<12} {:<10} {:<12} {:<6} {:<6} {:<6} {:<6}"
    print(row_fmt.format(*headers))
    print("-" * 80)

    for idx, name in enumerate(["Semantic (mpnet)", "TF-IDF Baseline"]):
        p, r, f1 = _precision_recall_f1(tp[idx], fp[idx], fn[idx])
        print(row_fmt.format(
            name,
            f"{p:.4f}", f"{r:.4f}", f"{f1:.4f}",
            tp[idx], fp[idx], fn[idx], tn[idx],
        ))


if __name__ == "__main__":
    main()
