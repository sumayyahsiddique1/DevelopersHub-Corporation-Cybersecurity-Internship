# OWASP Top 10 Compliance — DevelopersHub Corporation Internship

## Application: Python Flask Cybersecurity Project
## Assessed: April 28, 2026

---

| #   | Risk                              | Status     | Control Applied                                          |
|-----|-----------------------------------|------------|----------------------------------------------------------|
| A01 | Broken Access Control             | ✅ Fixed   | API Key authentication + route protection decorators     |
| A02 | Cryptographic Failures            | ✅ Fixed   | HTTPS enforced via HSTS with 1-year max-age              |
| A03 | Injection (SQLi, XSS)             | ✅ Fixed   | Prepared statements (SQLi) + CSP headers (XSS)           |
| A04 | Insecure Design                   | ✅ Fixed   | Rate limiting + CSRF token protection                    |
| A05 | Security Misconfiguration         | ✅ Fixed   | flask-talisman security headers applied globally         |
| A06 | Vulnerable & Outdated Components  | ✅ Checked | safety check + Trivy Docker image vulnerability scan     |
| A07 | Identification & Auth Failures    | ✅ Fixed   | API keys + CSRF session-bound tokens                     |
| A08 | Software & Data Integrity Failures| ✅ Fixed   | Dependency scanning with safety + bandit static analysis |
| A09 | Logging & Monitoring Failures     | ✅ Fixed   | Fail2Ban intrusion detection + monitor.py dashboard      |
| A10 | Server-Side Request Forgery       | ➖ N/A     | Not applicable to current application scope              |

---

## Notes

- A03 (Injection): sqli_demo.py demonstrates both the vulnerable f-string route
  and the secure prepared statement route side by side. bandit flags B608 on
  the vulnerable route, confirming the tool correctly identifies the risk.

- A06 (Vulnerable Components): `safety check` was run against all pip packages.
  `trivy image cybersec-app:v1` was run on the Docker image. Using python:3.11-slim
  as the base image minimises the number of installed packages and therefore CVEs.

- A09 (Logging & Monitoring): Fail2Ban is configured to ban IPs after 3 failed
  SSH login attempts. monitor.py provides a real-time Flask dashboard that tracks
  failed login attempts and raises alerts when the threshold is reached.
