from flask import Blueprint
from utils.response_utils import success

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    return success({"model_loaded": False, "version": "1.0.0"})
