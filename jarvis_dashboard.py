#!/usr/bin/env python3
import sqlite3
import os
import sys
import time

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def clear_screen():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

def run_dashboard():
    if not os.path.exists(DB_PATH):
        print("[❌] Dashboard Error: System database matrix uninitialized.")
        return

    while True:
        try:
            clear_screen()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            print("=" * 70)
            print(" ⚡  J.A.R.V.I.S.  INTERNAL REAL-TIME SYSTEM TELEMETRY CONTROL  ⚡ ")
            print("=" * 70)
            
            try:
                cursor.execute("SELECT COUNT(*) FROM outbound_pitch_staging;")
                pending = cursor.fetchone()[0]
            except: pending = 0
            
            try:
                cursor.execute("SELECT COUNT(*) FROM jarvis_business_logs WHERE directive_executed = 'STOREFRONT_CLIENT_OPENED';")
                total_opens = cursor.fetchone()[0]
            except: total_opens = 0
            
            print(f" STATUS INDEX :: Pending Broadcasts: {pending}  |  Total Monitored Opens: {total_opens}")
            print("-" * 70)
            print(f" {'TIMESTAMP':<22} | {'ENGAGED CLIENT TRAFFIC STATUS LINK':<45}")
            print("-" * 70)
            
            try:
                cursor.execute("""
                    SELECT raw_payload FROM jarvis_business_logs 
                    WHERE directive_executed = 'STOREFRONT_CLIENT_OPENED' 
                    ORDER BY id DESC LIMIT 15;
                """)
                rows = cursor.fetchall()
            except: rows = []
            
            if not rows:
                print("  [⚠️] Zero client telemetry pings registered in operational logs yet.")
            else:
                for row in rows:
                    log_text = row[0]
                    if "]" in log_text:
                        ts, msg = log_text.split("]", 1)
                        ts = ts.strip("[")
                        clean_msg = msg.replace("Telemetry Ping Recieved: ", "").strip()
                        print(f" {ts:<22} | {clean_msg:<45}")
                    else:
                        print(f" Unknown TS             | {log_text}")
                        
            print("=" * 70)
            print(" [Ctrl+C] to Exit | Automatically refreshing system parameters every 5s...")
            conn.close()
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n[-] Dashboard view terminated.")
            break
        except Exception as e:
            print(f"[❌] Telemetry UI error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_dashboard()
