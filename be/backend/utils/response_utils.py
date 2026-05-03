from flask import jsonify


def success(data: dict, status_code: int = 200):
    return jsonify({"status": "success", **data}), status_code


def error(code: str, message: str, status_code: int = 400):
    return jsonify({"status": "error", "code": code, "message": message}), status_code
