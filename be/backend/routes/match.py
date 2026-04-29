import time
from flask import Blueprint, request
from middleware.auth import require_token
from utils.response_utils import success, error
from models.db_models import get_db, Job
from services.embedding_service import compute_match
from services.baseline_service import compute_keyword_score, build_score_comparison

match_bp = Blueprint("match", __name__)


@match_bp.route("/match", methods=["POST"])
@require_token
def match():
    start = time.time()
    body = request.get_json(silent=True) or {}

    job_id = body.get("job_id", "")
    candidate_id = body.get("candidate_id", "")
    candidate_name = body.get("candidate_name", "")
    cv_text = body.get("cv_text", "")

    if not isinstance(job_id, str) or not job_id.strip():
        return error("INVALID_INPUT", "job_id is required.", 400)
    if not isinstance(candidate_id, str) or not candidate_id.strip():
        return error("INVALID_INPUT", "candidate_id is required.", 400)
    if not isinstance(candidate_name, str) or not candidate_name.strip():
        return error("INVALID_INPUT", "candidate_name is required.", 400)
    if not isinstance(cv_text, str) or not cv_text.strip():
        return error("INVALID_INPUT", "cv_text must not be empty.", 400)

    db = get_db()
    job = db.query(Job).filter(Job.id == job_id.strip()).first()
    if not job:
        return error("JOB_NOT_FOUND", f"No job found with id '{job_id}'.", 404)

    jd_dict = {
        "required_skills": job.skills_list(),
        "description": job.description,
        "required_education": job.required_education or "",
        "required_experience_years": job.required_experience_years,
    }
    jd_full_text = job.description + " " + " ".join(job.skills_list())

    try:
        # Stub placeholders (replaced in BE-021 with real NLP calls).
        language_detected = "unknown"
        cv_sections = {"skills": cv_text, "experience": cv_text, "education": cv_text}
        matched_skills = []
        missing_skills = jd_dict["required_skills"]
        detected_education = None
        years_detected = None

        scores = compute_match(cv_sections, jd_dict)
        keyword_score = compute_keyword_score(cv_text, jd_full_text)
        score_comparison = build_score_comparison(scores["semantic_score"], keyword_score)

        semantic = scores["semantic_score"]
        if semantic >= 80:
            grade = "High Match"
        elif semantic >= 60:
            grade = "Medium Match"
        else:
            grade = "Low Match"
    except Exception:
        return error("PROCESSING_ERROR", "An unexpected error occurred.", 500)

    elapsed = round((time.time() - start) * 1000)

    return success({
        "job_id": job.id,
        "job_title": job.title,
        "candidate_id": candidate_id.strip(),
        "candidate_name": candidate_name.strip(),
        "language_detected": language_detected,
        "grade": grade,
        "score_comparison": score_comparison,
        "breakdown": {
            "skills": {
                "score": scores["skills_score"],
                "weight": 0.4,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            },
            "experience": {
                "score": scores["experience_score"],
                "weight": 0.4,
                "years_detected": years_detected,
                "years_required": jd_dict["required_experience_years"],
            },
            "education": {
                "score": scores["education_score"],
                "weight": 0.2,
                "detected": detected_education,
                "required": jd_dict["required_education"],
            },
        },
        "processing_time_ms": elapsed,
    })