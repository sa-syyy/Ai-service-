from flask_limiter import Limiter

limiter = Limiter(
    key_func=lambda: "fixed-key",   # 🔥 force same bucket ALWAYS
    default_limits=["5 per minute"],
    storage_uri="memory://"
)