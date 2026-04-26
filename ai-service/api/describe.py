from flask import Flask, request, jsonify
from services.groq_client import GroqClient
from services.chroma_service import ChromaService
import json

app = Flask(__name__)

# 🔹 Initialize services
groq = GroqClient()
chroma = ChromaService()

# 🔥 Add initial data (so DB is not empty)
chroma.add_text("Unauthorized transaction detected", "1")
chroma.add_text("Payment failed due to network error", "2")


@app.route('/')
def home():
    return "API is running"


# 🔹 Day 3 — Categorise
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


# 🔥 Day 5 — RAG Query API
@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question = data.get("question")

        # 🔹 Step 1: Get similar docs
        results = chroma.query_with_docs(question)
        docs = results["documents"]

        # 🔹 Step 2: Build context
        context = "\n".join(docs)

        # 🔹 Step 3: Create prompt
        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

        # 🔹 Step 4: Call Groq
        response = groq.generate_response(prompt)

        return jsonify({
            "answer": response,
            "sources": docs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)