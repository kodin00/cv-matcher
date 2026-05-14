from flask import Blueprint, request
from middleware.auth import require_token
from utils.response_utils import success, error
from models.db_models import get_db, Job

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/jobs", methods=["GET"])
@require_token
def list_jobs():
    industry = request.args.get("industry")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    db = get_db()
    query = db.query(Job)

    if industry:
        query = query.filter(Job.industry == industry)

    total = query.count()
    jobs = query.offset((page - 1) * limit).limit(limit).all()

    return success({
        "total": total,
        "page": page,
        "limit": limit,
        "jobs": [
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "industry": job.industry,
                "required_experience_years": job.required_experience_years,
                "created_at": job.created_at,
            }
            for job in jobs
        ],
    })


@jobs_bp.route("/jobs/<job_id>", methods=["GET"])
@require_token
def get_job(job_id):
    db = get_db()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return error("JOB_NOT_FOUND", f"No job found with id '{job_id}'.", 404)

    return success({
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "industry": job.industry,
        "description": job.description,
        "required_skills": job.skills_list(),
        "required_experience_years": job.required_experience_years,
        "required_education": job.required_education,
        "created_at": job.created_at,
    })
