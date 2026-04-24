from flask import Flask, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

# Store failed attempts in memory (for demo)
failed_attempts = {}
ALERT_THRESHOLD = 3

def parse_fail2ban_log():
    """Read Fail2Ban log and return recent bans"""
    bans = []
    try:
        with open('/var/log/fail2ban.log', 'r') as f:
            for line in f:
                if 'Ban' in line:
                    bans.append(line.strip())
    except FileNotFoundError:
        bans = ["Log file not found — Fail2Ban may not have triggered yet"]
    return bans[-10:]  # Return last 10 bans

@app.route('/monitor', methods=['GET'])
def monitor():
    """Dashboard showing recent bans"""
    bans = parse_fail2ban_log()
    return jsonify({
        "status": "Monitoring Active",
        "recent_bans": bans,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/login-attempt', methods=['POST'])
def track_login():
    """Simulate tracking failed login attempts"""
    data = request.get_json()
    ip = request.remote_addr
    success = data.get('success', False)

    if not success:
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        count = failed_attempts[ip]

        if count >= ALERT_THRESHOLD:
            return jsonify({
                "alert": f"⚠️ ALERT: IP {ip} has failed {count} times!",
                "action": "This IP would be banned by Fail2Ban"
            }), 429

        return jsonify({
            "message": f"Failed attempt {count}/{ALERT_THRESHOLD} from {ip}"
        }), 401

    failed_attempts[ip] = 0
    return jsonify({"message": "Login successful"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
