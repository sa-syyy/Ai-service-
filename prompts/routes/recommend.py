import json
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json.get("input")

    with open("prompts/recommend.txt") as f:
        prompt = f.read().replace("{input}", data)

    result = call_groq(prompt)

    try:
        parsed = json.loads(result)   # ✅ convert string → JSON
        return jsonify(parsed)
    except:
        return jsonify({
            "error": "Invalid JSON from AI",
            "raw": result
        })