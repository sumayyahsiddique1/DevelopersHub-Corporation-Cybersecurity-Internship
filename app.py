from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import secrets
import os

app = Flask(__name__)

# -----------------------------------------------
# 1. CORS — Only allow your trusted frontend
# -----------------------------------------------
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],  # your frontend URL only
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "X-API-KEY"]
    }
})

# -----------------------------------------------
# 2. RATE LIMITING — Prevent brute force
# -----------------------------------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per minute"]
)

# -----------------------------------------------
# 3. API KEY AUTH — Simple but effective
# -----------------------------------------------
VALID_API_KEYS = {
    "intern-key-123": "intern_user",
    "admin-key-456": "admin_user"
}

def require_api_key(f):
    """Decorator to protect routes with API key"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key not in VALID_API_KEYS:
            abort(401)  # Unauthorized
        return f(*args, **kwargs)
    return decorated

# -----------------------------------------------
# PUBLIC ROUTE — No auth needed
# -----------------------------------------------
@app.route('/api/public')
@limiter.limit("5 per minute")  # Stricter limit for public
def public_route():
    return jsonify({"message": "This is public data"})

# -----------------------------------------------
# PROTECTED ROUTE — Requires API key
# -----------------------------------------------
@app.route('/api/secure-data')
@limiter.limit("20 per minute")
@require_api_key
def secure_data():
    user = VALID_API_KEYS[request.headers.get('X-API-KEY')]
    return jsonify({
        "message": "You have access!",
        "user": user,
        "secret_data": "Top secret info here 🔒"
    })

# -----------------------------------------------
# ERROR HANDLERS
# -----------------------------------------------
@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Invalid or missing API key"}), 401

@app.errorhandler(429)
def ratelimit_exceeded(e):
    return jsonify({"error": "Rate limit exceeded. Slow down!"}), 429

if __name__ == '__main__':
    app.run(debug=True, port=5000)
