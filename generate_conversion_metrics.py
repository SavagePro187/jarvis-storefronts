#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def print_dynamic_metrics():
    print("\n[======================== JARVIS POLYMORPHIC REVENUE MATRIX ========================]")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM income_stream_registry;")
    total_streams = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT r.operation_type,
               r.search_query_template,
               COUNT(s.id) as total_processed,
               SUM(CASE WHEN s.status='sent' THEN 1 ELSE 0 END) as delivered,
               SUM(CASE WHEN s.status='quarantined' THEN 1 ELSE 0 END) as quarantined
        FROM income_stream_registry r
        LEFT JOIN outbound_pitch_staging s ON r.operation_type = s.operation_type
        GROUP BY r.operation_type;
    """)
    rows = cursor.fetchall()
    
    print(f"Active Algorithmic Engines: {total_streams}\n")
    print(f"{'DIGITAL INCOME VECTOR':<25} | {'TOTAL LEADS':<12} | {'DELIVERED':<10} | {'QUARANTINED':<12}")
    print("-" * 80)
    
    for row in rows:
        op_type, query, total, sent, quarantined = row
        print(f"{op_type:<25} | {total:<12} | {sent:<10} | {quarantined:<12}")
        
    print("[===================================================================================]\n")
    conn.close()

if __name__ == "__main__":
    print_dynamic_metrics()
