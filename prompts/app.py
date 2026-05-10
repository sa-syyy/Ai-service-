from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "running"})

@app.route("/test")
def test():
    return jsonify({"message": "API is working"})

# AI Describe API
@app.route("/describe", methods=["POST"])
def describe():
    data = request.json
    user_input = data.get("text")

    return jsonify({
        "response": f"AI description for: {user_input}"
    })

# AI Recommend API
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_input = data.get("text")

    return jsonify({
        "response": f"AI recommendation for: {user_input}"
    })

# ✅ KEEP THIS LAST
if __name__ == "__main__":
    app.run(debug=True)