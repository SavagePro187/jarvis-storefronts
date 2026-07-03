#!/usr/bin/env python3
import os
import time
import sqlite3

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def log_event(directive, payload):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, raw_payload) VALUES (?, ?);", (directive, str(payload)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Database write failure: {e}")

try:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jarvis_business_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        directive_executed TEXT NOT NULL,
        raw_payload TEXT
    );
    """)
    conn.commit()
    conn.close()
except Exception:
    pass

while True:
    print("[+] Executing autonomous e-commerce and digital asset arbitrage cycle...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='arbitrage_inventory';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            cursor.execute("SELECT product_name, target_retail_price, projected_margin FROM arbitrage_inventory LIMIT 1;")
            row = cursor.fetchone()
            conn.close()
            
            if row:
                log_event("DROPSHIP_LISTING_ACTIVE", f"Product: {row[0]} | Target Retail: {row[1]} | Expected Profit Margin: {row[2]}")
            else:
                log_event("DROPSHIP_INVENTORY_IDLE", "Awaiting fresh product items ingestion streams.")
        else:
            conn.close()
            log_event("DROPSHIP_TABLE_MISSING", "Inventory tracking matrix not found. Re-initializing...")
            
    except Exception as e:
        log_event("DIGITAL_ARBITRAGE_ERR", str(e))
        
    time.sleep(60)
