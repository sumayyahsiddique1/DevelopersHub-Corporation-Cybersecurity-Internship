from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "demo.db"

# -------------------------------------------------------
# DATABASE SETUP — Create a demo database with users
# -------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@test.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'pass456', 'alice@test.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'bob',   'pass789', 'bob@test.com')")
    conn.commit()
    conn.close()

# -------------------------------------------------------
# VULNERABLE ROUTE — Direct string formatting (UNSAFE)
# An attacker can input: ' OR '1'='1  to dump all users
# -------------------------------------------------------
@app.route('/login/vulnerable', methods=['GET'])
def login_vulnerable():
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # DANGEROUS — never do this in real code!
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"[VULNERABLE] Executing: {query}")

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "Login successful (VULNERABLE route)",
            "user": {"id": user[0], "username": user[1], "email": user[3]},
            "warning": "This route is vulnerable to SQL injection!"
        })
    return jsonify({"status": "Login failed"}), 401


# -------------------------------------------------------
# SECURE ROUTE — Prepared statements (SAFE)
# User input is treated as data, never as SQL code
# -------------------------------------------------------
@app.route('/login/secure', methods=['GET'])
def login_secure():
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SAFE — ? placeholders prevent SQL injection entirely
    query = "SELECT * FROM users WHERE username=? AND password=?"
    print(f"[SECURE] Executing with params: ({username}, {password})")

    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "Login successful (SECURE route)",
            "user": {"id": user[0], "username": user[1], "email": user[3]},
            "note": "Protected by prepared statements"
        })
    return jsonify({"status": "Login failed"}), 401


if __name__ == '__main__':
    init_db()
    print("Database initialized with demo users")
    print("Vulnerable route: http://localhost:5000/login/vulnerable")
    print("Secure route:     http://localhost:5000/login/secure")
    app.run(debug=True, port=5000)
