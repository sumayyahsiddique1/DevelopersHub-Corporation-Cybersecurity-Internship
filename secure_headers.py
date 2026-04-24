from flask import Flask, jsonify
from flask_talisman import Talisman

app = Flask(__name__)

# -----------------------------------------------
# CONTENT SECURITY POLICY (CSP)
# Prevents script injection / XSS attacks
# -----------------------------------------------
csp = {
    'default-src': "'self'",           # Only load from your own domain
    'script-src': ["'self'"],          # No inline scripts allowed
    'style-src': ["'self'"],           # No inline styles allowed
    'img-src': ["'self'", "data:"],    # Images from self or data URIs
    'connect-src': "'self'",           # API calls only to self
    'frame-ancestors': "'none'",       # No iframes (prevents clickjacking)
}

# -----------------------------------------------
# TALISMAN — Applies ALL security headers at once
# Includes: HSTS, CSP, X-Frame-Options, etc.
# -----------------------------------------------
Talisman(
    app,
    content_security_policy=csp,
    force_https=False,           # Set True in real production!
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,  # 1 year
    x_content_type_options=True,
    x_xss_protection=True,
)

@app.route('/')
def home():
    return jsonify({
        "message": "Secured endpoint ✅",
        "headers_active": [
            "Content-Security-Policy",
            "Strict-Transport-Security (HSTS)",
            "X-Content-Type-Options",
            "X-XSS-Protection",
            "X-Frame-Options"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
