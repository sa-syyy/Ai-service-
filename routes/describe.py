from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

describe_bp = Blueprint('describe', __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = request.json.get("input")

    with open("prompts/describe.txt") as f:
        prompt = f.read().replace("{input}", data)

    result = call_groq(prompt)

    return jsonify({"result": result})
