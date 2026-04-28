from flask import Flask, request, jsonify, session, render_template_string
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.csrf import CSRFError
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)

# -------------------------------------------------------
# SECRET KEY — Required for sessions and CSRF tokens
# -------------------------------------------------------
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['WTF_CSRF_ENABLED'] = True

# -------------------------------------------------------
# CSRF PROTECTION — Protects all POST requests globally
# -------------------------------------------------------
csrf = CSRFProtect(app)

# -------------------------------------------------------
# SIMPLE FORM WITH CSRF TOKEN
# -------------------------------------------------------
class UpdateProfileForm(FlaskForm):
    username  = StringField('Username',  validators=[DataRequired()])
    email     = StringField('Email',     validators=[DataRequired()])
    submit    = SubmitField('Update Profile')

# -------------------------------------------------------
# HTML TEMPLATE — Form includes hidden CSRF token
# -------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>CSRF Demo — DevelopersHub Cybersecurity Internship</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
    h2 { color: #2E75B6; }
    input { padding: 8px; margin: 5px 0; width: 100%; box-sizing: border-box; }
    button { background: #2E75B6; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
    hr { margin: 30px 0; }
    .note { background: #f0f4ff; border-left: 4px solid #2E75B6; padding: 10px; }
  </style>
</head>
<body>
  <h2>Update Profile (CSRF Protected)</h2>
  <div class="note">This form includes a hidden CSRF token. Requests without a valid token are rejected with 403.</div>
  <br>
  <form method="POST" action="/update-profile">
    {{ form.hidden_tag() }}
    <label>Username:</label>
    <input name="username" type="text" placeholder="Enter username"/>
    <label>Email:</label>
    <input name="email" type="text" placeholder="Enter email"/>
    <button type="submit">Update Profile</button>
  </form>

  <hr>
  <h2>API Endpoints for Testing</h2>
  <ul>
    <li>GET <code>/csrf-token</code> — Retrieve a valid CSRF token</li>
    <li>POST <code>/update-profile</code> — Protected (requires CSRF token)</li>
    <li>POST <code>/update-profile/unprotected</code> — Vulnerable (no CSRF check)</li>
  </ul>
</body>
</html>
"""

# -------------------------------------------------------
# ROUTES
# -------------------------------------------------------
@app.route('/')
def index():
    form = UpdateProfileForm()
    return render_template_string(HTML_TEMPLATE, form=form)

@app.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    """Returns a valid CSRF token for API/Burp Suite testing"""
    from flask_wtf.csrf import generate_csrf
    token = generate_csrf()
    return jsonify({
        "csrf_token": token,
        "usage": "Include this in X-CSRFToken header or csrf_token form field"
    })

@app.route('/update-profile', methods=['POST'])
def update_profile():
    """Protected profile update — requires valid CSRF token"""
    form = UpdateProfileForm()
    if form.validate_on_submit():
        return jsonify({
            "status": "Profile updated successfully",
            "username": form.username.data,
            "email": form.email.data,
            "csrf": "Token was valid — request is legitimate"
        })
    return jsonify({
        "status": "Request blocked",
        "reason": "Invalid or missing CSRF token",
        "error": str(form.errors)
    }), 403

@app.route('/update-profile/unprotected', methods=['POST'])
@csrf.exempt  # This route has NO CSRF protection — for demo comparison
def update_profile_unprotected():
    """Unprotected route — vulnerable to CSRF attacks"""
    username = request.form.get('username', 'unknown')
    email    = request.form.get('email', 'unknown')
    return jsonify({
        "status": "Profile updated (UNPROTECTED route)",
        "username": username,
        "email": email,
        "warning": "This route has NO CSRF protection — vulnerable to forged requests!"
    })

# -------------------------------------------------------
# ERROR HANDLER — When CSRF token is invalid/missing
# -------------------------------------------------------
@app.errorhandler(CSRFError)
def csrf_error(e):
    return jsonify({
        "error": "CSRF token missing or invalid",
        "detail": str(e),
        "blocked": True
    }), 403

if __name__ == '__main__':
    print("CSRF Demo running at http://localhost:5000")
    print("Protected form:       http://localhost:5000/")
    print("Get CSRF token:       http://localhost:5000/csrf-token")
    print("Protected endpoint:   POST http://localhost:5000/update-profile")
    print("Unprotected endpoint: POST http://localhost:5000/update-profile/unprotected")
    app.run(debug=True, port=5000)
