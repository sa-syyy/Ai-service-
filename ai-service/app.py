from flask import Flask, jsonify
from routes.describe import describe_bp
from routes.generate_report import generate_bp
from extensions import limiter   # ✅ import from new file

app = Flask(__name__)

limiter.init_app(app)
app.config["RATELIMIT_HEADERS_ENABLED"] = True  

app.register_blueprint(describe_bp)
app.register_blueprint(generate_bp)

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "retry_after": str(e.description)
    }), 429

if __name__ == "__main__":
    app.run(debug=True)