from flask import Blueprint
from utils.response_utils import success
from services.embedding_service import is_model_loaded

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    return success({"model_loaded": is_model_loaded(), "version": "1.0.0"})
