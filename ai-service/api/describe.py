from flask import Flask, request, jsonify
from services.groq_client import GroqClient
from services.chroma_service import ChromaService
import json
import time

app = Flask(__name__)

# 🔹 Initialize services
groq = GroqClient()
chroma = ChromaService()

# 🔥 Day 7 — Tracking variables
APP_START_TIME = time.time()
RESPONSE_TIMES = []

# Placeholder cache stats (Day 8 will replace with Redis)
CACHE_HITS = 0
CACHE_MISSES = 0


# 🔥 Initial data
chroma.add_text("Unauthorized transaction detected", "1")
chroma.add_text("Payment failed due to network error", "2")
chroma.add_text("Payment stuck but money deducted", "3")
chroma.add_text("App crashes during login due to server timeout", "4")
chroma.add_text("Account blocked due to suspicious activity", "5")


@app.route('/')
def home():
    return "API is running"


# 🔹 Utility function
def track_response_time(start_time):
    global RESPONSE_TIMES
    duration = (time.time() - start_time) * 1000
    RESPONSE_TIMES.append(duration)

    if len(RESPONSE_TIMES) > 10:
        RESPONSE_TIMES.pop(0)


# 🔹 Categorise
@app.route('/categorise', methods=['POST'])
def categorise():
    start_time = time.time()

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
            parsed = {"raw_response": response}

        track_response_time(start_time)

        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 RAG Query
@app.route('/query', methods=['POST'])
def query():
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question = data.get("question")

        results = chroma.query_with_docs(question)

        documents = []
        if results and "documents" in results:
            documents = results["documents"]

        if not documents:
            track_response_time(start_time)
            return jsonify({
                "answer": "No relevant data found",
                "sources": []
            })

        context = "\n".join(documents)

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

        response = groq.generate_response(prompt)

        track_response_time(start_time)

        return jsonify({
            "answer": response.strip(),
            "sources": documents
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 Day 7 — HEALTH ENDPOINT
@app.route('/health', methods=['GET'])
def health():
    try:
        uptime = int(time.time() - APP_START_TIME)

        avg_response = (
            sum(RESPONSE_TIMES) / len(RESPONSE_TIMES)
            if RESPONSE_TIMES else 0
        )

        doc_count = chroma.get_count()

        return jsonify({
            "status": "healthy",
            "model": groq.model,
            "avg_response_time_ms": round(avg_response, 2),
            "last_10_responses": [round(t, 2) for t in RESPONSE_TIMES],
            "chroma_doc_count": doc_count,
            "uptime_seconds": uptime,
            "cache": {
                "hits": CACHE_HITS,
                "misses": CACHE_MISSES
            }
        })

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)