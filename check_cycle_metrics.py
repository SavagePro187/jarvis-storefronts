#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def audit_pipeline_execution():
    if not os.path.exists(DB_PATH):
        print("[❌] Status Query Aborted: System database initialization absent.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("="*60)
    print("⚡ J.A.R.V.I.S. AUTOMATED FUNNEL STATUS SUMMARY AUDIT ⚡")
    print("="*60)
    
    # 1. Check logged lead arrays
    try:
        cursor.execute("SELECT COUNT(*) FROM jarvis_business_logs WHERE directive_executed = 'LEAD_SCRAPER_RUN_SUCCESS';")
        logs_count = cursor.fetchone()[0]
        print(f"🔹 Scraper Blocks Dispatched to Logs : {logs_count} payload runs")
    except sqlite3.OperationalError:
        print("🔹 Scraper Blocks Dispatched to Logs : 0 records (Table structure uninitialized)")

    # 2. Check staged copy vectors
    try:
        cursor.execute("SELECT operation_type, COUNT(*) FROM outbound_pitch_staging GROUP BY operation_type;")
        staged_rows = cursor.fetchall()
        print("\n🔹 Staged Personalization Vectors Pending Delivery Vector Routing:")
        if not staged_rows:
            print("  [⚠️] Zero records currently staged inside outbound_pitch_staging.")
        for row in staged_rows:
            print(f"  ▪ [{row[0]}]: {row[1]} targeted accounts validated and ready.")
    except sqlite3.OperationalError:
        print("\n  [❌] Staging structure missing or completely empty.")
        
    print("="*60)
    conn.close()

if __name__ == "__main__": audit_pipeline_execution()
