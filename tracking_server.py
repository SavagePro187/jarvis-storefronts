#!/usr/bin/env python3
import sqlite3
import os
import time
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

class TelemetryHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress standard console noise to keep log streams clean

    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        # Intercept incoming traffic hitting the telemetry route
        if parsed_url.path == '/track':
            params = parse_qs(parsed_url.query)
            company_slug = params.get('company', ['unknown'])[0]
            
            # Format clean logging block
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log_entry = f"[{timestamp}] Telemetry Ping Recieved: Company slug '{company_slug}' accessed private proposal storefront."
            print(f" 🔔 [VISIT DETECTED] {log_entry}")
            
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO jarvis_business_logs (directive_executed, raw_payload)
                    VALUES ('STOREFRONT_CLIENT_OPENED', ?);
                """, (log_entry,))
                conn.commit()
                conn.close()
            except Exception as db_err:
                print(f" [❌] Telemetry database save failure: {db_err}")

            # Send a ultra-lightweight transparent response pixel back to the browser
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.send_header('Access-Control-Allow-Origin', '*') # Permit wide cross-origin telemetry
            self.end_headers()
            # 1x1 Transparent GIF pixel payload data
            self.wfile.write(b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b')
            return
            
        self.send_response(404)
        self.end_headers()

def run_telemetry_node():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, TelemetryHandler)
    print("="*60)
    print("⚡ J.A.R.V.I.S. TELEMETRY LISTENER ONLINE -> PORT 5000 ⚡")
    print("="*60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Telemetry engine halting safely.")
        httpd.server_close()

if __name__ == '__main__':
    run_telemetry_node()
