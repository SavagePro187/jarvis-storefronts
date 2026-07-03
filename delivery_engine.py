#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import os
import time

def load_native_env(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

env_path = os.path.expanduser("~/Projects/active/jarvishive/.env")
load_native_env(env_path)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

SUBJECT_ROUTING = {
    "B2B_LEAD_GEN": "Scaling Automation Infrastructure Matrix - {comp}",
    "SAAS_COLD_OUTREACH": "Technical Infrastructure Optimization Matrix - {comp}",
    "AGENCY_ARBITRAGE": "Strategic Growth Infrastructure Scaling - {comp}"
}

def dispatch_approved_queue():
    if not all([EMAIL_USER, EMAIL_PASS]):
        print("[-] Missing email credentials inside .env file configuration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company_name, target_email, customized_pitch, operation_type 
        FROM outbound_pitch_staging 
        WHERE status = 'approved';
    """)
    queued_nodes = cursor.fetchall()

    if not queued_nodes:
        print("[+] Active send queue is empty. Zero approved records found.")
        conn.close()
        return

    print(f"[+] Initializing dispatch sequence for {len(queued_nodes)} verified targets...")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30.0)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
    except Exception as e:
        print(f"[-] Could not establish network link with SMTP relay: {e}")
        conn.close()
        return

    for node in queued_nodes:
        r_id, comp, email_addr, body_content, op_type = node
        print(f"[+] Routing customized message dispatch to {comp} ({email_addr}) via [{op_type}]...")

        msg = MIMEMultipart()
        msg['From'] = f"SAVAGE PRODUCTION COMPANY LLC <{EMAIL_USER}>"
        msg['To'] = email_addr
        
        subject_template = SUBJECT_ROUTING.get(op_type, "Corporate Scaling Vectors - {comp}")
        msg['Subject'] = subject_template.format(comp=comp)
        
        msg.attach(MIMEText(body_content, 'plain', 'utf-8'))

        try:
            server.sendmail(EMAIL_USER, email_addr, msg.as_string())
            cursor.execute("UPDATE outbound_pitch_staging SET status = 'sent' WHERE id = ?;", (r_id,))
            conn.commit()
            print(f"    [SUCCESS] Message successfully delivered. Node {r_id} status marked sent.")
            time.sleep(2)
        except Exception as send_err:
            print(f"    [-] Failed to transfer payload data packet: {send_err}")

    server.quit()
    conn.close()
    print("[+] All approved outbound pipeline queues processed.")

if __name__ == "__main__":
    dispatch_approved_queue()
