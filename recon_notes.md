# Week 5 — Reconnaissance Results

## Target: testphp.vulnweb.com
## Date: April 28, 2026
## Tool: Kali Linux (VirtualBox)

---

## WHOIS Results

| Field               | Value                                      |
|---------------------|--------------------------------------------|
| Domain              | vulnweb.com                                |
| Registrar           | Gandi SAS                                  |
| Created             | 2010-06-14                                 |
| Expires             | 2027-06-14                                 |
| Name Servers        | ns-105-a.gandi.net, ns-11-b.gandi.net      |
| DNSSEC              | Unsigned (not cryptographically verified)  |

---

## DNS Lookup Results

| Record Type | Value                                              |
|-------------|--------------------------------------------------- |
| A           | 44.228.249.3                                       |
| rDNS        | ec2-44-228-249-3.us-west-2.compute.amazonaws.com   |
| TXT         | google-site-verification token found               |
| TTL         | 3146 seconds (~52 minutes)                         |
| Hosting     | Amazon AWS — US-West (Oregon)                      |

**Finding:** Site is hosted on AWS EC2. rDNS reveals cloud infrastructure details.

---

## Nmap Port Scan Results

All 1000 TCP ports filtered — server is behind AWS Security Groups / WAF.

| Port | State    | Reason                          |
|------|----------|---------------------------------|
| All  | Filtered | AWS firewall blocking TCP probes|

**Finding:** Firewall/WAF active. No open ports detected via standard SYN scan.
This is a legitimate security finding — port scanning prevention is best practice.

---

## HTTP Headers (curl -I)

Run: `curl -I https://testphp.vulnweb.com`

Document your actual output here after running the command.

---

## Notes

- Standard Nmap SYN scans blocked by AWS Security Groups
- Nikto requires HTTPS: `nikto -h https://testphp.vulnweb.com`
- SQLMap target: `http://testphp.vulnweb.com/listproducts.php?cat=1`
