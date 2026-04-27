from flask import Flask, request, jsonify
from services.groq_client import GroqClient
from services.chroma_service import ChromaService
import json

app = Flask(__name__)

# 🔹 Initialize services
groq = GroqClient()
chroma = ChromaService()

# 🔥 Initial data (expanded for better retrieval)
chroma.add_text("Unauthorized transaction detected", "1")
chroma.add_text("Payment failed due to network error", "2")
chroma.add_text("Payment stuck but money deducted", "3")
chroma.add_text("App crashes during login due to server timeout", "4")
chroma.add_text("Account blocked due to suspicious activity", "5")


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


# 🔥 Day 5 + Day 6 — RAG Query API (FIXED + IMPROVED)
@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question = data.get("question")

        # 🔹 Step 1: Retrieve documents from ChromaDB
        results = chroma.query_with_docs(question)

        # 🔥 SAFE extraction of documents
        documents = []
        if results and "documents" in results:
            if len(results["documents"]) > 0:
                documents = results["documents"][0]

        # 🔹 Step 2: Handle no results
        if not documents:
            return jsonify({
                "answer": "No relevant data found",
                "sources": []
            })

        # 🔹 Step 3: Build context
        context = "\n".join(documents)

        # 🔹 Step 4: Prompt tuning (Day 6 improvement)
        prompt = f"""
Answer the question using ONLY the context below.

Rules:
- Answer in 1 short line
- Do NOT explain
- Do NOT add extra information

Context:
{context}

Question:
{question}
"""

        # 🔹 Step 5: Call LLM
        response = groq.generate_response(prompt)

        # 🔹 Step 6: Return clean structured response
        return jsonify({
            "answer": response.strip(),
            "sources": documents
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)