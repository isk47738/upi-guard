#!/usr/bin/env python3
"""
UPI Guard - Multi-terminal Shared UTR Server (Hackathon Backend)
Pure Python Standard Library (Zero External Dependencies)
"""
import http.server
import socketserver
import socket
import sqlite3
import json
import os
import sys
from datetime import datetime

PORT = 8000
DB_FILE = os.path.join(os.path.dirname(__file__), "transactions.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS verified_utrs (
            utr TEXT PRIMARY KEY,
            amount TEXT,
            app TEXT,
            terminal_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Pre-populate demo fraud UTR
    c.execute('INSERT OR IGNORE INTO verified_utrs (utr, amount, app, terminal_id) VALUES (?, ?, ?, ?)',
              ("432501984211", "150.00", "Google Pay", "Counter_1"))
    conn.commit()
    conn.close()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class UPIGuardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(302)
            self.send_header('Location', '/fast_scanner.html')
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/verify_utr':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            utr = data.get('utr', '').strip()
            amount = data.get('amount', '')
            app = data.get('app', '')
            terminal = data.get('terminal', 'Counter_Mobile')

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('SELECT timestamp, terminal_id, amount FROM verified_utrs WHERE utr = ?', (utr,))
            row = c.fetchone()

            response = {}
            if row:
                response = {
                    "status": "DUPLICATE_REUSED",
                    "valid": False,
                    "first_seen": row[0],
                    "claimed_at_terminal": row[1],
                    "message": f"ALERT: UTR {utr} was already redeemed at {row[1]} on {row[0]}!"
                }
            else:
                c.execute('INSERT INTO verified_utrs (utr, amount, app, terminal_id) VALUES (?, ?, ?, ?)',
                          (utr, amount, app, terminal))
                conn.commit()
                response = {
                    "status": "UNIQUE_RECORDED",
                    "valid": True,
                    "message": f"UTR {utr} registered successfully as genuine transaction."
                }
            conn.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    init_db()
    local_ip = get_local_ip()
    print("=" * 65)
    print("🛡️   UPI Guard - Fake UPI Screenshot Detector Server")
    print("=" * 65)
    print(f"💻  Laptop Browser (Direct):  http://localhost:{PORT}")
    print(f"📱  Phone Access (Hotspot):   http://{local_ip}:{PORT}")
    print("=" * 65)
    print("💡 AGAR PHONE ME LINK NA KHULE:")
    print("   1. Phone ka Mobile Hotspot ON karo aur Laptop connect karo.")
    print("   2. Phir phone me http://<naya_hotspot_ip>:8000 dalo.")
    print("   (Campus/Hostel Wi-Fi security devices ko aapas me block karta hai)")
    print("=" * 65)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UPIGuardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            sys.exit(0)
