#!/usr/bin/env python3
import json
import sqlite3
import os
import sys
import time

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def bridge_scraped_agency_leads(source_json_path):
    if not os.path.exists(source_json_path):
        print(f"[❌] Source payload file missing: {source_json_path}")
        return False
        
    try:
        with open(source_json_path, 'r') as f:
            scraped_data = json.load(f)
    except Exception as e:
        print(f"[❌] Malformed JSON structure inside source file: {e}")
        return False

    # Standardize data wrapper structure matching the master orchestrator token pattern
    log_payload = {
        "operation_type": "AGENCY_ARBITRAGE",
        "timestamp": int(time.time()),
        "leads": scraped_data.get("leads", scraped_data) # Safe fallback if root is list
    }

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ensure log storage framework layout exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jarvis_business_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            directive_executed TEXT,
            raw_payload TEXT
        );
        """)
        
        # Insert log array with token signature matching core generation system boundaries
        cursor.execute("""
            INSERT INTO jarvis_business_logs (directive_executed, raw_payload)
            VALUES ('LEAD_SCRAPER_RUN_SUCCESS', ?);
        """, (json.dumps(log_payload),))
        
        conn.commit()
        print(f"[✔] Successfully bridged {len(log_payload['leads'])} agency nodes into jarvis_business_logs.")
        conn.close()
        return True
    except Exception as e:
        print(f"[❌] Database pipeline insertion crash: {e}")
        return False

if __name__ == "__main__":
    # Expects path to scraper output JSON file as an argument
    target_json = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Projects/active/jarvishive/scraped_agencies.json")
    bridge_scraped_agency_leads(target_json)
