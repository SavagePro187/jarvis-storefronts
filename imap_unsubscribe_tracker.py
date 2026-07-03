#!/usr/bin/env python3
import imaplib
import email
import sqlite3
import os
import re
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

# 1. Initialize configuration tokens
env_path = os.path.expanduser("~/Projects/active/jarvishive/.env")
load_native_env(env_path)

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def connect_imap():
    if not all([IMAP_SERVER, EMAIL_USER, EMAIL_PASS]):
        print("[-] Missing environmental configurations. Check your .env file structure.")
        return None
    try:
        print(f"[+] Connecting to IMAP server ({IMAP_SERVER}) via native env mapping...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except Exception as e:
        print(f"[-] Authentication failed: {e}")
        return None

def process_unsubscribes():
    mail = connect_imap()
    if not mail:
        return

    mail.select("inbox")
    
    # SAFE COMPLIANCE FILTER: Track explicit opt-out intent keywords ONLY in the Subject Header line
    compliance_keywords = ["REMOVE", "UNSUBSCRIBE", "STOP", "OPT OUT"]
    all_email_ids = set()

    for keyword in compliance_keywords:
        # Changed from global 'TEXT' to strict 'SUBJECT' to prevent scraping irrelevant emails
        status, messages = mail.search(None, f'(UNSEEN SUBJECT "{keyword}")')
        if status == "OK" and messages and messages[0]:
            all_email_ids.update(messages[0].split())

    if not all_email_ids:
        print("[+] No new compliance or unsubscribe requests found.")
        mail.logout()
        return

    print(f"[+] Found {len(all_email_ids)} unique targeted subject-line opt-out messages.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for e_id in all_email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        if status != "OK":
            continue

        raw_email = msg_data[0][1] if isinstance(msg_data[0], tuple) else msg_data[0]
        msg = email.message_from_bytes(raw_email)
        
        from_header = msg.get("From", "")
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_header)
        
        if email_match:
            unsub_email = email_match.group(0).lower().strip()
            print(f"[!] Processing compliance opt-out from: {unsub_email}")
            
            # Step A: Drop immediate targets from outbound staging queues
            cursor.execute("DELETE FROM outbound_pitch_staging WHERE target_email = ?;", (unsub_email,))
            deleted_rows = cursor.rowcount
            
            # Step B: Record globally to prevent future background scrapers from processing this node
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS global_suppression_list (
                        email TEXT PRIMARY KEY,
                        unsubscribed_at INTEGER
                    );
                """)
                cursor.execute("INSERT OR IGNORE INTO global_suppression_list (email, unsubscribed_at) VALUES (?, ?);", 
                               (unsub_email, int(time.time())))
                conn.commit()
            except Exception as db_err:
                print(f"[-] Suppression database error: {db_err}")

            if deleted_rows > 0:
                print(f"    [CLEANED] Successfully purged target node from active staging pipelines.")
            else:
                print(f"    [SECURED] Node added directly to global safety suppression blocks.")
            
            # Mark the message as read to prevent infinite loop reprocessing
            mail.store(e_id, '+FLAGS', '\\Seen')
        else:
            print(f"[-] Unable to resolve sender address string layout: {from_header}")

    conn.close()
    mail.logout()
    print("[+] Compliance sweep completed successfully.")

if __name__ == "__main__":
    process_unsubscribes()
