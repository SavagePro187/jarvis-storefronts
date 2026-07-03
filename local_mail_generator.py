#!/usr/bin/env python3
import os
import urllib.parse
import glob
import subprocess
import sys
import sqlite3

outreach_dir = os.path.expanduser("~/Desktop/ai_workspace/ready_outreach")
DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
pitch_files = glob.glob(os.path.join(outreach_dir, "*_pitch.txt"))

def log_event(directive, payload):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jarvis_business_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                directive_executed TEXT NOT NULL,
                payload_data TEXT
            );
        """)
        cursor.execute("""
            INSERT INTO jarvis_business_logs (directive_executed, payload_data)
            VALUES (?, ?);
        """, (directive, str(payload)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[!] DB Log Fail: {e}")
        return False

if not pitch_files:
    print("No pitches found.")
    sys.exit(0)

print(f"Found {len(pitch_files)} pitch files to process.\n")

for index, file_path in enumerate(pitch_files, start=1):
    filename = os.path.basename(file_path)
    print(f"[{index}/{len(pitch_files)}] Next file: {filename}")
    
    response = input("Press [Enter] to open in Mail.app (or 'q' to quit, 's' to skip): ").strip().lower()
    if response == 'q':
        print("Exiting pipeline execution.")
        break
    elif response == 's':
        print(f"Skipping {filename}.\n")
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if len(lines) < 3:
            continue
            
        to_email = lines[0].replace("TO:", "").strip()
        subject = lines[1].replace("SUBJECT:", "").strip()
        body = "".join(lines[2:]).strip()
        body = body.replace('\r\n', '\n').replace('\r', '\n')

        query_params = {'subject': subject, 'body': body}
        url_args = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
        mailto_url = f"mailto:{to_email}?{url_args}"

        subprocess.run(["open", mailto_url], check=True)
        log_event("EMAIL_DRAFT_OPENED", f"Sent pitch blueprint out to {to_email}")
        print(f" [✔] Opened draft window for {to_email}.\n")
        
    except Exception as e:
        print(f" Error processing {filename}: {e}\n")

print("[✔] Processing loop complete.")
