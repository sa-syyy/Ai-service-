import re
import bleach
from flask import request, jsonify

BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"bypass security",
    r"act as",
    r"drop table",
    r"select \* from"
]

def clean_html(text):
    return bleach.clean(text, tags=[], strip=True)

def is_malicious(text):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def sanitize_request():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    cleaned_data = {}

    for key, value in data.items():
        if isinstance(value, str):
            value = clean_html(value)

            if is_malicious(value):
                return jsonify({
                    "error": f"Malicious input detected in field: {key}"
                }), 400

            cleaned_data[key] = value
        else:
            cleaned_data[key] = value

    request.cleaned_data = cleaned_data