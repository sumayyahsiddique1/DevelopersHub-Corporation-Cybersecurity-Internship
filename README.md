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
DevelopersHub-Corporation-Cybersecurity-Internship/
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
├── requirements.txt            # All Python dependencies
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
Perform active reconnaissance on a legally sanctioned target, exploit a SQL injection vulnerability using SQLMap, build a vulnerable + secure demo app to illustrate the fix, and implement CSRF protection with Flask-WTF.

---

### ✅ Features Implemented

#### 🔍 1. Reconnaissance on testphp.vulnweb.com (Task 1)

Target: `testphp.vulnweb.com` — a site intentionally built for security testing by Acunetix.

**Tools used:** `whois`, `nslookup`, `dig`, `nmap`, `nikto`, `curl`

**Key Findings:**

| Finding                | Detail                                                        |
|------------------------|---------------------------------------------------------------|
| IP Address             | 44.228.249.3                                                  |
| Hosting                | Amazon AWS EC2 — US-West-2 (Oregon)                          |
| Domain Registrar       | Gandi SAS (France)                                            |
| Domain Created         | June 14, 2010                                                 |
| DNSSEC                 | Unsigned — DNS responses not cryptographically verified       |
| Google Verification    | TXT record found (Google site-verification)                   |
| Nmap Port Scan         | All 1000 TCP ports filtered — blocked by AWS Security Groups |
| Nmap Finding           | WAF/firewall active; cloud infrastructure exposed via rDNS    |

```bash
# WHOIS
whois vulnweb.com

# DNS Lookup
nslookup testphp.vulnweb.com
dig testphp.vulnweb.com
dig testphp.vulnweb.com ANY

# Port Scan
nmap testphp.vulnweb.com
nmap -sV testphp.vulnweb.com
nmap -Pn -p 80,443 testphp.vulnweb.com

# Web Vulnerability Scan
nikto -h https://testphp.vulnweb.com

# HTTP Headers
curl -I https://testphp.vulnweb.com
```

All recon output saved to `week5-reports/recon_notes.md`.

---

#### 💉 2. SQL Injection — SQLMap + Prepared Statement Fix (Task 2)

**SQLMap commands run against testphp.vulnweb.com:**

```bash
# Basic scan — detect injection point
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch

# Enumerate all databases
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --dbs

# List tables in acuart database
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch -D acuart --tables

# Dump users table
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch -D acuart -T users --dump
```

**SQLi Fix — `sqli_demo.py`** implements both a vulnerable and a secure route side-by-side:

| Route                    | Method           | SQL Injection | Result                        |
|--------------------------|------------------|---------------|-------------------------------|
| `/login/vulnerable`      | f-string query   | ❌ Unsafe      | Bypassed with `' OR '1'='1`  |
| `/login/secure`          | Prepared `?` params | ✅ Safe    | Injection blocked             |

```bash
# Test vulnerable route — injection works
curl "http://localhost:5000/login/vulnerable?username=admin&password=' OR '1'='1"

# Test secure route — injection blocked
curl "http://localhost:5000/login/secure?username=admin&password=' OR '1'='1"
```

---

#### 🛡️ 3. CSRF Protection with Flask-WTF (Task 3)

**File: `csrf_demo.py`**

| Route                         | CSRF Protected | Behaviour                              |
|-------------------------------|----------------|----------------------------------------|
| `POST /update-profile`        | ✅ Yes          | Blocked with 403 if token missing      |
| `POST /update-profile/unprotected` | ❌ No     | Accepts any POST — vulnerable          |
| `GET /csrf-token`             | N/A            | Returns valid token for API testing    |

**Test commands:**

```bash
# Test 1 — POST without CSRF token (BLOCKED — 403)
curl -X POST http://localhost:5000/update-profile \
  -d "username=hacker&email=hacker@evil.com"

# Test 2 — Get a valid token
TOKEN=$(curl -s http://localhost:5000/csrf-token | python3 -c "import sys,json; print(json.load(sys.stdin)['csrf_token'])")

# Test 3 — POST with valid token (SUCCESS)
curl -X POST http://localhost:5000/update-profile \
  -d "username=alice&email=alice@test.com&csrf_token=$TOKEN"

# Test 4 — Unprotected route — no token needed (VULNERABLE)
curl -X POST http://localhost:5000/update-profile/unprotected \
  -d "username=hacker&email=hacker@evil.com"
```

---

### 🔐 Week 5 Security Outcomes

| Task                       | Tool / Method                       | Status  |
|----------------------------|-------------------------------------|---------|
| Recon — WHOIS              | whois                               | ✅ Done |
| Recon — DNS                | nslookup, dig                       | ✅ Done |
| Recon — Port Scan          | nmap -sV                            | ✅ Done |
| Recon — Web Vuln Scan      | nikto                               | ✅ Done |
| SQLi — Exploit             | sqlmap --dbs, --tables, --dump      | ✅ Done |
| SQLi — Vulnerable Demo     | sqli_demo.py /login/vulnerable      | ✅ Done |
| SQLi — Secure Fix          | sqli_demo.py /login/secure          | ✅ Done |
| CSRF — Protection          | flask-wtf CSRFProtect               | ✅ Done |
| CSRF — Tested              | curl + Burp Suite                   | ✅ Done |
| GitHub repo updated        | git push                            | ✅ Done |

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/DevelopersHub-Corporation-Cybersecurity-Internship.git
cd DevelopersHub-Corporation-Cybersecurity-Internship

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
```

---

## 📅 Week 6 — Coming Soon

> Security Audits, OWASP ZAP, Secure Deployment, Final Penetration Test

---

*DevelopersHub Corporation Cybersecurity Internship — 2026*
