#!/usr/bin/env python3
import os
import time
import sqlite3
import random

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

NICHES = ["roofer", "epoxy flooring", "hvac repair", "landscaping"]
CITIES = ["covina", "west covina", "glendora", "azusa", "pomona"]
HOOKS = ["emergency", "affordable", "commercial", "top-rated"]

def log_event(directive, payload):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, raw_payload) VALUES (?, ?);", (directive, str(payload)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Database write failure: {e}")

while True:
    print("[+] Executing long-tail SMB keyword prospecting algorithm...")
    try:
        # Programmatically construct high-intent long-tail search phrases
        niche = random.choice(NICHES)
        city = random.choice(CITIES)
        hook = random.choice(HOOKS)
        long_tail_keyword = f"{hook} {niche} in {city} ca"
        
        # Structure a custom, zero-risk performance marketing offer payload
        pitch_payload = {
            "target_keyword": long_tail_keyword,
            "business_footprint": "Low (Missing site mapping / unoptimized listing)",
            "offer_structure": f"We will rank a dedicated lead generation page for the keyword phrase '{long_tail_keyword}' at our own expense. You only pay a flat performance fee per exclusive booked customer call we route to your phone. Zero upfront cost.",
            "status": "Staged for transmission"
        }
        
        log_event("SMB_PROSPECT_GENERATED", pitch_payload)
    except Exception as e:
        log_event("SMB_PROSPECT_ERR", str(e))
    time.sleep(60)
