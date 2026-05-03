from functools import wraps
from flask import request
from utils.response_utils import error
from config import APP_TOKEN


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not APP_TOKEN:
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer ") or auth_header[7:] != APP_TOKEN:
            return error("UNAUTHORIZED", "Invalid or missing token.", 401)
        return f(*args, **kwargs)
    return decorated
