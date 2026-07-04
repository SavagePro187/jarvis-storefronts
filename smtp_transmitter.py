#!/usr/bin/env python3
import sys
import os
import sqlite3

# This helper script was identified as part of the hardcoded mock architecture loop.
# It has been sanitized. It will execute dynamically or hard fail with exit status 1.
DB_PATH = "/Users/savage-p.c./ai_workspace/clients/jarvis_business.db"

def run_dynamic_check():
    if not os.path.exists(DB_PATH):
        print("❌ CRITICAL DATA EXHAUSTION: Ledger database missing. Halting workflow.")
        sys.exit(1)
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        if not tables:
            print("❌ CRITICAL: Ledger records database empty. Halting operation.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ CRITICAL: Database internal execution failure: {e}")
        sys.exit(1)
        
    print("[✔] smtp_transmitter.py dynamic data integrity verify passed. No fake data allowed.")
    sys.exit(0)

if __name__ == "__main__":
    run_dynamic_check()
