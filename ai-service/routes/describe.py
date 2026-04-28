from flask import Blueprint, request, jsonify
from middleware.sanitizer import sanitize_request

describe_bp = Blueprint("describe", __name__)

@describe_bp.before_request
def before():
    result = sanitize_request()
    if result:
        return result

@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = getattr(request, "cleaned_data", {})  # safer access

    return jsonify({
        "message": "Describe API working",
        "cleaned_data": data
    })