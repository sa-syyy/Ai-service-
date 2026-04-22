from flask import Flask, request, jsonify
from services.groq_client import GroqClient

app = Flask(__name__)

# Initialize Groq client
groq = GroqClient()


@app.route('/')
def home():
    return "API is running"


@app.route('/describe', methods=['POST'])
def describe():
    try:
        data = request.get_json()

        # Input validation
        if not data or "input" not in data:
            return jsonify({
                "error": "Missing 'input' in request body"
            }), 400

        user_input = data.get("input")

        # Call Groq service
        response = groq.generate_response(user_input)

        return jsonify({
            "response": response
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)