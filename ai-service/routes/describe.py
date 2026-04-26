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
    data = request.cleaned_data
    return jsonify({"cleaned_data": data})