from flask import Flask, request, jsonify
from services.groq_client import GroqClient
import json

app = Flask(__name__)

groq = GroqClient()


@app.route('/')
def home():
    return "API is running"


@app.route('/categorise', methods=['POST'])
def categorise():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({
            "error": "Missing 'input' in request body"
        }), 400

    user_input = data.get("input")

    try:
        prompt = f"""
Classify the following text into one of these categories:
fraud, finance, technical, general, complaint

Return ONLY JSON:
{{
  "category": "...",
  "confidence": 0.0,
  "reasoning": "..."
}}

Text: {user_input}
"""

        response = groq.generate_response(prompt)

        # 🔥 CLEAN JSON parsing
        try:
            parsed = json.loads(response)
        except:
            parsed = {
                "raw_response": response
            }

        return jsonify(parsed)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)