# DevelopersHub Corporation — Cybersecurity Internship

> A hands-on cybersecurity internship project focused on building, securing, and auditing web applications using industry-standard tools and best practices on Kali Linux.

---

## 👨‍💻 Intern Information

| Field        | Details                                              |
|--------------|------------------------------------------------------|
| Organization | DevelopersHub Corporation                            |
| Program      | Cybersecurity Internship                             |
| Duration     | Weeks 4–6 (April–May 2026)                          |
| Stack        | Python 3, Flask, Kali Linux (VirtualBox)             |
| GitHub Repo  | DevelopersHub-Corporation-Cybersecurity-Internship   |

---

## 📁 Project Structure

```
DevelopersHub-Corporation-Cybersecurity-Internship-W4ToW6/
│
├── Week 4 — Threat Detection & Web Security
│   ├── monitor.py              # Fail2Ban log parser + failed login alert tracker
│   ├── app.py                  # Rate limiting + CORS + API key authentication
│   └── secure_headers.py       # CSP, HSTS, XSS protection headers
│
├── Week 5 — Ethical Hacking & Exploitation
│   ├── sqli_demo.py            # SQL injection demo (vulnerable vs secure routes)
│   ├── csrf_demo.py            # CSRF protection with Flask-WTF
│   └── week5-reports/
│       ├── recon_notes.md      # WHOIS, DNS, Nmap findings
│       ├── nikto_report.txt    # Nikto web vulnerability scan output
│       └── sqlmap_output/      # SQLMap scan results directory
│
├── Week 6 — Security Audits & Final Deployment
│   ├── Dockerfile              # Hardened Docker container for Flask app
│   ├── .dockerignore           # Excludes sensitive files from image
│   └── week6-reports/
│       ├── zap_report.html     # OWASP ZAP web application scan report
│       ├── nikto_week6.txt     # Nikto scan — Week 6 comparison run
│       ├── nikto_flask.txt     # Nikto scan against Flask app
│       ├── lynis_report.txt    # Lynis Linux system security audit
│       ├── bandit_report.txt   # Bandit Python static code analysis
│       ├── trivy_report.txt    # Trivy Docker image vulnerability scan
│       ├── metasploit_report.txt # Metasploit auxiliary scan results
│       └── owasp_compliance.md # OWASP Top 10 compliance checklist
│
├── requirements.txt            # All Python dependencies
├── Weeks4_5_6_Cybersecurity_Report.docx  # Full implementation report
└── README.md
```

---

## 📅 Week 4 — Advanced Threat Detection & Web Security

### 🎯 Goal
Implement real-time intrusion detection, harden API endpoints against common attack vectors, and enforce HTTP security headers on a Python Flask application.

---

### ✅ Features Implemented

#### 🔍 1. Intrusion Detection & Monitoring (`monitor.py`)
- Configured **Fail2Ban** to monitor `/var/log/auth.log` in real time
- Auto-bans IPs after **3 failed login attempts** within 5 minutes (10 min ban duration)
- Built a Python Flask dashboard to parse Fail2Ban logs and display recent bans
- Alert system returns `429 Too Many Requests` when an IP exceeds the threshold
- Tested with `curl` — confirmed graduated warnings and final ban alert

#### 🔒 2. API Security Hardening (`app.py`)
- **Rate limiting** via `flask-limiter` — 10 requests/minute, 100/day per IP
- **CORS** restricted to `http://localhost:3000` only (trusted frontend)
- **API Key authentication** decorator protecting sensitive routes
- Public route accessible without key; protected route requires `X-API-KEY` header
- `401 Unauthorized` returned for missing/invalid keys
- `429 Too Many Requests` returned on rate limit breach

#### 🛡️ 3. Security Headers & CSP (`secure_headers.py`)
- **Content Security Policy (CSP)** — blocks script injections, inline JS, and untrusted origins
- **HSTS** (Strict-Transport-Security) — 1-year max-age, enforces HTTPS
- `X-Frame-Options: DENY` — prevents clickjacking via iframes
- `X-Content-Type-Options: nosniff` — prevents MIME-type sniffing
- `X-XSS-Protection` — legacy browser XSS filter
- All headers applied globally using `flask-talisman`

---

### 🛠️ Week 4 Tech Stack

| Tool / Library    | Purpose                              |
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

### 🔐 Week 4 Security Outcomes

| Threat                  | Protection Applied                  | Status  |
|-------------------------|-------------------------------------|---------|
| Brute-force login       | Fail2Ban + rate limiting            | ✅ Done |
| Unauthorized API access | API Key authentication              | ✅ Done |
| Cross-origin attacks    | CORS restricted to trusted origins  | ✅ Done |
| Script injection (XSS)  | Content Security Policy (CSP)       | ✅ Done |
| Protocol downgrade      | HSTS enforced                       | ✅ Done |
| Clickjacking            | X-Frame-Options: DENY               | ✅ Done |

---

## 📅 Week 5 — Ethical Hacking & Exploitation

### 🎯 Goal
Perform active reconnaissance on a legally sanctioned target, exploit a SQL injection vulnerability using SQLMap, build a vulnerable and secure demo app to illustrate the fix, and implement CSRF protection with Flask-WTF.

---

### ✅ Features Implemented

#### 🕵️ 1. Reconnaissance on testphp.vulnweb.com

Target: `testphp.vulnweb.com` — a site intentionally built for security testing by Acunetix.

**Tools used:** `whois`, `nslookup`, `dig`, `nmap`, `nikto`, `curl`

| Finding             | Detail                                                        |
|---------------------|---------------------------------------------------------------|
| IP Address          | 44.228.249.3                                                  |
| Hosting             | Amazon AWS EC2 — US-West-2 (Oregon)                          |
| Domain Registrar    | Gandi SAS (France)                                            |
| Domain Created      | June 14, 2010                                                 |
| DNSSEC              | Unsigned — DNS responses not cryptographically verified       |
| Nmap Port Scan      | All 1000 TCP ports filtered — blocked by AWS Security Groups |
| Nmap Finding        | WAF/firewall active; cloud infrastructure confirmed via rDNS  |

#### 💉 2. SQL Injection — SQLMap + Prepared Statement Fix

- Set up **DVWA** (Damn Vulnerable Web Application) locally on Apache + MySQL
- Used **SQLMap** against DVWA — confirmed **time-based blind** and **UNION query** injection
- Dumped the full `users` table including usernames and MD5 hashed passwords
- Built `sqli_demo.py` to show the attack on a vulnerable Flask route vs a secure route using **prepared statements**

| Route               | Method              | SQL Injection | Result                       |
|---------------------|---------------------|---------------|------------------------------|
| `/login/vulnerable` | f-string query      | ❌ Unsafe      | Bypassed with `' OR '1'='1` |
| `/login/secure`     | Prepared `?` params | ✅ Safe        | Injection blocked            |

#### 🛡️ 3. CSRF Protection with Flask-WTF

- Implemented **CSRF token validation** on all POST routes using `flask-wtf`
- Built `csrf_demo.py` with a protected route and an unprotected route for comparison
- Requests without a valid CSRF token are rejected with **403 Forbidden**

---

### 🔐 Week 5 Security Outcomes

| Task                       | Tool / Method                  | Status  |
|----------------------------|--------------------------------|---------|
| Recon — WHOIS              | whois                          | ✅ Done |
| Recon — DNS                | nslookup, dig                  | ✅ Done |
| Recon — Port Scan          | nmap -sV                       | ✅ Done |
| Recon — Web Vuln Scan      | nikto (DVWA)                   | ✅ Done |
| SQLi — Exploit             | sqlmap --dbs, --tables, --dump | ✅ Done |
| SQLi — Vulnerable Demo     | sqli_demo.py /login/vulnerable | ✅ Done |
| SQLi — Secure Fix          | sqli_demo.py /login/secure     | ✅ Done |
| CSRF — Protection          | flask-wtf CSRFProtect          | ✅ Done |
| CSRF — Tested              | curl + Burp Suite              | ✅ Done |

---

## 📅 Week 6 — Advanced Security Audits & Final Deployment

### 🎯 Goal
Conduct advanced security audits against the application and system, verify OWASP Top 10 compliance, containerise the application using Docker with security best practices, scan for vulnerabilities, and perform a final penetration test.

---

### ✅ Features Implemented

#### 🔍 1. Security Audits & Compliance

**OWASP ZAP** — automated web application vulnerability scan against DVWA and the Flask app:
- Identified missing security headers, insecure cookies, and potential XSS vectors in DVWA
- Flask app passed significantly better due to flask-talisman headers applied in Week 4
- Full report saved to `week6-reports/zap_report.html`

**Nikto** — web server scan (Week 6 comparison run):
- Re-ran against DVWA and Flask app to compare with Week 5 findings
- Flask app now shows CSP, HSTS, and X-Content-Type-Options present
- Confirms Week 4 security headers are effective

**Lynis** — full Linux system security audit:
- Audited kernel hardening, file permissions, authentication, and network settings
- Produces a Hardening Index score out of 100
- All suggestions and warnings saved to `week6-reports/lynis_report.txt`

**Python Security Scanning:**
- `safety check` — scanned all installed packages against known CVE database
- `bandit` — static analysis of Python code for security issues
- Confirmed `sqli_demo.py` correctly flags B608 (SQL string formatting) on the vulnerable route

**OWASP Top 10 Compliance:**

| # | Risk                        | Status    | Control Applied                              |
|---|-----------------------------|-----------|----------------------------------------------|
| A01 | Broken Access Control     | ✅ Fixed  | API Key auth + route protection              |
| A02 | Cryptographic Failures    | ✅ Fixed  | HTTPS enforced via HSTS                      |
| A03 | Injection                 | ✅ Fixed  | Prepared statements + CSP                    |
| A04 | Insecure Design           | ✅ Fixed  | Rate limiting + CSRF tokens                  |
| A05 | Security Misconfiguration | ✅ Fixed  | flask-talisman headers globally applied      |
| A06 | Vulnerable Components     | ✅ Checked | safety check + Trivy image scan             |
| A07 | Auth & Session Failures   | ✅ Fixed  | API keys + CSRF session-bound tokens         |
| A08 | Software Integrity        | ✅ Fixed  | Dependency scanning with safety + bandit     |
| A09 | Logging & Monitoring      | ✅ Fixed  | Fail2Ban + monitor.py dashboard              |
| A10 | SSRF                      | ➖ N/A    | Not applicable to current app scope          |

---

#### 🐳 2. Secure Docker Deployment

Docker was used to containerise the Flask application with the following security best practices applied:

| Practice                     | Applied | How                                              |
|------------------------------|---------|--------------------------------------------------|
| Official slim base image     | ✅      | `python:3.11-slim` — minimal attack surface      |
| Run as non-root user         | ✅      | Created `appuser` — `USER appuser` in Dockerfile |
| Read-only filesystem         | ✅      | `--read-only` flag on `docker run`               |
| No privilege escalation      | ✅      | `--no-new-privileges` flag                       |
| No secrets in image          | ✅      | `.dockerignore` excludes `.env` and `.db` files  |
| Image vulnerability scan     | ✅      | Trivy scan on `cybersec-app:v1`                  |
| Health check configured      | ✅      | `HEALTHCHECK` in Dockerfile — 30s interval       |
| Minimal dependencies only    | ✅      | `--no-cache-dir`, only `requirements.txt` packages |
| Auto security updates on host| ✅      | `unattended-upgrades` enabled                    |

```bash
# Build the image
docker build -t cybersec-app:v1 .

# Scan with Trivy
trivy image cybersec-app:v1

# Run securely
docker run -d \
  --name cybersec-container \
  --read-only \
  --no-new-privileges \
  -p 5000:5000 \
  cybersec-app:v1
```

---

#### 💀 3. Final Penetration Testing

**Metasploit Framework:**
- Initialised `msfdb` and launched `msfconsole`
- Ran auxiliary modules: HTTP version scanner, TCP port scanner, directory scanner
- Results saved to `week6-reports/metasploit_report.txt`

**Burp Suite:**
- Configured Firefox to proxy through Burp on `127.0.0.1:8080`
- Intercepted and analysed all DVWA and Flask app requests
- Sent requests to Repeater to manually test for injection and CSRF weaknesses
- Confirmed CSRF protection — removing `csrf_token` from POST body returns `403 Forbidden`
- Ran active scanner via Dashboard — findings saved to Issues tab

---

### 🛠️ Week 6 Tech Stack

| Tool              | Purpose                                    |
|-------------------|--------------------------------------------|
| OWASP ZAP         | Web application vulnerability scanning     |
| Nikto             | Web server vulnerability scanning          |
| Lynis             | Linux system security auditing             |
| Docker            | Application containerisation               |
| Trivy             | Docker image CVE scanning                  |
| Metasploit        | Auxiliary penetration testing              |
| Burp Suite        | HTTP proxy + web application scanner       |
| safety            | Python dependency CVE checking             |
| bandit            | Python static code security analysis       |
| unattended-upgrades | Automatic system security updates        |

---

### 🔐 Week 6 Security Outcomes

| Task                               | Tool                          | Status  |
|------------------------------------|-------------------------------|---------|
| OWASP ZAP scan (DVWA + Flask)      | zaproxy                       | ✅ Done |
| Nikto scan (DVWA + Flask)          | nikto                         | ✅ Done |
| Lynis system audit                 | lynis                         | ✅ Done |
| Python dependency scan             | safety + bandit               | ✅ Done |
| OWASP Top 10 compliance check      | Manual checklist              | ✅ Done |
| Auto security updates enabled      | unattended-upgrades           | ✅ Done |
| Dockerfile created (hardened)      | docker build                  | ✅ Done |
| Docker image vulnerability scan    | trivy                         | ✅ Done |
| Container run with security flags  | docker run                    | ✅ Done |
| Metasploit auxiliary scan          | msfconsole                    | ✅ Done |
| Burp Suite final scan + CSRF test  | burpsuite                     | ✅ Done |
| GitHub repo updated                | git push                      | ✅ Done |

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/sumayyahsiddique1/DevelopersHub-Corporation-Cybersecurity-Internship-W4ToW6.git
cd DevelopersHub-Corporation-Cybersecurity-Internship-W4ToW6

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run Week 4 modules
python3 monitor.py          # Intrusion detection dashboard (port 5000)
python3 app.py              # Rate limiting + CORS + API key auth (port 5000)
python3 secure_headers.py   # Security headers active (port 5000)

# 5. Run Week 5 modules
python3 sqli_demo.py        # SQLi vulnerable vs secure demo (port 5000)
python3 csrf_demo.py        # CSRF protection demo (port 5000)

# 6. Run Week 6 Docker deployment
docker build -t cybersec-app:v1 .
docker run -d --name cybersec-container --read-only --no-new-privileges -p 5000:5000 cybersec-app:v1
```

---

*DevelopersHub Corporation Cybersecurity Internship — 2026*
