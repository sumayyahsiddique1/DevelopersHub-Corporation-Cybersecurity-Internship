# DevelopersHub Corporation - Cybersecurity Internship

> A hands-on cybersecurity internship project focused on building, securing, and auditing web applications using industry-standard tools and best practices.

---

## 👨‍💻 Intern Information

| Field        | Details                        |
|--------------|-------------------------------|
| Organization | DevelopersHub Corporation      |
| Program      | Cybersecurity Internship       |
| Duration     | Weeks 4–6 (April–May 2026)    |
| Stack        | Python, Flask, Kali Linux      |

---

## 📅 Week 4: Advanced Threat Detection & Web Security

### 🎯 Goal
Implement advanced security measures, detect threats in real-time, and secure API endpoints against common attack vectors.

---

### ✅ Features Implemented

#### 🔍 1. Intrusion Detection & Monitoring
- Configured **Fail2Ban** to monitor system logs in real-time
- Auto-bans IPs after **3 failed login attempts** within 5 minutes
- Built a Python Flask dashboard (`monitor.py`) to visualize active bans and login attempts
- Integrated alert system that returns warnings as failed attempts accumulate

#### 🔒 2. API Security Hardening
- Applied **rate limiting** using `flask-limiter` — max 10 requests/minute per IP
- Configured **CORS** to only allow requests from trusted frontend origins
- Implemented **API Key authentication** to protect sensitive endpoints
- Unauthorized requests return `401 Unauthorized` with a clear error message
- Rate-exceeded requests return `429 Too Many Requests`

#### 🛡️ 3. Security Headers & CSP
- Implemented **Content Security Policy (CSP)** to block script injections and XSS
- Enforced **HSTS** (Strict-Transport-Security) with 1-year max-age
- Added `X-Frame-Options` to prevent clickjacking
- Added `X-Content-Type-Options` and `X-XSS-Protection` headers
- All headers applied globally using `flask-talisman`

---

### 🛠️ Tech Stack

| Tool/Library      | Purpose                              |
|-------------------|--------------------------------------|
| Python 3          | Core programming language            |
| Flask             | Web framework for API development    |
| Fail2Ban          | Intrusion detection & IP banning     |
| flask-limiter     | API rate limiting                    |
| flask-cors        | Cross-Origin Resource Sharing config |
| flask-talisman    | Security headers (CSP, HSTS, etc.)   |
| pyotp             | One-time password / 2FA support      |
| Kali Linux        | Security-focused OS environment      |

---

### 📁 Project Structure

```
DevelopersHub-Corporation-Cybersecurity-Internship/
│
├── monitor.py              # Fail2Ban log parser + failed login alert tracker
├── app.py                  # Main API — rate limiting, CORS, API key auth
├── secure_headers.py       # Security headers — CSP, HSTS, XSS protection
├── requirements.txt        # All Python dependencies
└── README.md               # Project documentation
```

---

### ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/DevelopersHub-Corporation-Cybersecurity-Internship.git
cd DevelopersHub-Corporation-Cybersecurity-Internship

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run any module
python3 monitor.py        # Intrusion detection dashboard
python3 app.py            # Secured API with rate limiting & auth
python3 secure_headers.py # API with security headers active
```

---

### 🧪 Testing the API

```bash
# ✅ Test public route (no auth needed)
curl http://localhost:5000/api/public

# ✅ Test protected route WITH valid API key
curl http://localhost:5000/api/secure-data \
  -H "X-API-KEY: intern-key-123"

# ❌ Test protected route WITHOUT key (should return 401)
curl http://localhost:5000/api/secure-data

# ⚠️ Test rate limiting — run 6 times to trigger 429
for i in {1..6}; do curl http://localhost:5000/api/public; done

# 🔍 Test login alert system (run 4 times to trigger alert)
curl -X POST http://localhost:5000/login-attempt \
  -H "Content-Type: application/json" \
  -d '{"success": false}'

# 📊 View monitoring dashboard
curl http://localhost:5000/monitor
```

---

### 🔐 Security Outcomes

| Threat                  | Protection Applied                  | Status |
|-------------------------|-------------------------------------|--------|
| Brute-force login       | Fail2Ban + rate limiting            | ✅ Done |
| Unauthorized API access | API Key authentication              | ✅ Done |
| Cross-origin attacks    | CORS restricted to trusted origins  | ✅ Done |
| Script injection (XSS)  | Content Security Policy (CSP)       | ✅ Done |
| Protocol downgrade      | HSTS enforced                       | ✅ Done |
| Clickjacking            | X-Frame-Options: DENY               | ✅ Done |

---

## 📅 Week 5 — Coming Soon
> Ethical Hacking, SQL Injection Testing, CSRF Protection

## 📅 Week 6 — Coming Soon
> Security Audits, OWASP ZAP, Secure Deployment, Final Pen Test

---

*DevelopersHub Corporation Cybersecurity Internship — 2026*
