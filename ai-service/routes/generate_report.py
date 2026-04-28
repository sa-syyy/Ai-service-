from flask import Blueprint, jsonify, request
from middleware.sanitizer import sanitize_request
from extensions import limiter 

generate_bp = Blueprint("generate", __name__)

@generate_bp.before_request
def before():
    result = sanitize_request()
    if result:
        return result

@generate_bp.route("/generate-report", methods=["POST"])
@limiter.limit("3 per minute")   
def generate_report():
    data = request.cleaned_data

    return jsonify({
        "message": "Report generated successfully",
        "data": data
    })