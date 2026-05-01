import json
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.chroma_client import query_docs

report_bp = Blueprint('report', __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json.get("input")

    # ✅ FIX 1: prevent None input
    if not data:
        return jsonify({"error": "Input is required"}), 400

    # ✅ FIX 2: safe RAG call
    try:
        context = query_docs(data)
    except:
        context = []

    with open("prompts/report.txt") as f:
        prompt = f.read().replace("{input}", data + "\nContext:" + str(context))

    result = call_groq(prompt)

    try:
        parsed = json.loads(result)
        return jsonify(parsed)
    except:
        return jsonify({
            "error": "Invalid JSON from AI",
            "raw": result
        })