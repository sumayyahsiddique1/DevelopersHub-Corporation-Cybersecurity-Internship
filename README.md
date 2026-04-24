# Cybersecurity Internship — Week 4

## Features Implemented
- ✅ Fail2Ban intrusion detection with real-time monitoring
- ✅ API rate limiting (flask-limiter)
- ✅ CORS restriction to trusted origins
- ✅ API Key authentication
- ✅ Security headers: CSP, HSTS, XSS Protection

## How to Run
```bash
pip3 install flask flask-limiter flask-cors flask-talisman
python3 app.py
```

## Files
- `monitor.py` — Fail2Ban log monitor + failed login tracker
- `app.py` — Rate limiting + CORS + API key auth
- `secure_headers.py` — CSP and security headers
