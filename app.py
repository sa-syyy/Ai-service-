from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "running"})

@app.route("/test")
def test():
    return jsonify({"message": "API is working"})

if __name__ == "__main__":
    app.run(debug=True)