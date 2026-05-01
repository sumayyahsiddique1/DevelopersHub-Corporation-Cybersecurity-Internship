# Docker Security Best Practices — DevelopersHub Internship Week 6

## Image: cybersec-app:v1
## Base: python:3.11-slim
## Assessed: April 28, 2026

---

| Practice                        | Applied | How                                                     |
|---------------------------------|---------|---------------------------------------------------------|
| Use official slim base image    | ✅      | python:3.11-slim — minimal packages, smaller CVE footprint |
| Run as non-root user            | ✅      | Created appuser group + user, switched with USER appuser |
| Read-only filesystem            | ✅      | --read-only flag passed to docker run                   |
| No privilege escalation         | ✅      | --no-new-privileges flag passed to docker run           |
| No sensitive data in image      | ✅      | .dockerignore excludes .env, *.db, venv/, .git/         |
| Image vulnerability scanning    | ✅      | trivy image cybersec-app:v1 run and report saved        |
| Health check configured         | ✅      | HEALTHCHECK in Dockerfile — 30s interval, 3 retries     |
| Minimal dependencies            | ✅      | pip install --no-cache-dir from requirements.txt only   |
| Auto security updates on host   | ✅      | unattended-upgrades installed and enabled               |

---

## Build Command
```bash
docker build -t cybersec-app:v1 .
```

## Scan Command
```bash
trivy image cybersec-app:v1
trivy image cybersec-app:v1 --severity CRITICAL,HIGH
```

## Secure Run Command
```bash
docker run -d \
  --name cybersec-container \
  --read-only \
  --no-new-privileges \
  -p 5000:5000 \
  cybersec-app:v1
```

## Verify
```bash
docker ps
curl http://localhost:5000/api/public
docker logs cybersec-container
```
