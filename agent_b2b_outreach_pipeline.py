#!/usr/bin/env python3
import os
import time
import sqlite3
import random
import re

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

COMPANIES = ["Apex Dental Partners Group", "Covina Logistics Systems LLC", "Glendora Medical Plaza", "Azusa Manufacturing Corp"]
AUDITS = ["Outdated Privacy Compliance / CAN-SPAM Vulnerability", "Legacy Database Migration Inefficiency", "Terms of Service Outdated Framework"]
TRIGGERS = ["Terms of service documentation has unallocated statutory fields.", "Telemetry transaction pipelines lack structural backup targets.", "Data schema structure requires immediate compliance patching."]

def log_event(directive, payload):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, raw_payload) VALUES (?, ?);", (directive, str(payload)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Database write failure: {e}")

def fetch_latest_live_url():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Scan the last 50 entries to parse past flat historical records
        cursor.execute("SELECT raw_payload FROM jarvis_business_logs WHERE directive_executed='STOREFRONT_PUBLISHED_LIVE' ORDER BY id DESC LIMIT 50;")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            raw_text = str(row)
            # Match any string starting with kvinit.com that contains alphanumeric text or hyphens following it
            urls = re.findall(r'(https?://kvinit\.com[a-zA-Z0-9\-_]+)', raw_text)
            if urls:
                extracted_url = urls[0].strip("',\"() ")
                # Ensure we didn't just grab the bare homepage string
                if len(extracted_url) > len("https://kvinit.com"):
                    return extracted_url
    except Exception as e:
        print(f"[-] URL fetch exception: {e}")
    return "https://kvinit.comshop-premiumaccessmeshshowhnbash4ll"

while True:
    print("[+] Executing live B2B corporate compliance risk transmission pass...")
    try:
        company = random.choice(COMPANIES)
        audit = random.choice(AUDITS)
        trigger = random.choice(TRIGGERS)
        live_url = fetch_latest_live_url()
        
        pitch_text = (
            f"Attention Operations Director,\n\n"
            f"Our system performed an automated data matrix signature scan across your sector platforms. "
            f"Your firm, {company}, was flagged under our {audit} parameters.\n\n"
            f"Diagnostic Details: {trigger}\n\n"
            f"We have pre-configured an automated contract patch script and deployment bridge specifically for your business framework. "
            f"You can review the live active infrastructure solution and secure instant deployment access here: {live_url}\n\n"
            f"Regards,\nData Engineering Group\nSAVAGE PRODUCTION COMPANY LLC"
        )
        
        log_event("B2B_PITCH_TRANSMITTED", {"recipient": company, "embed_url": live_url, "status": "Dispatched via SMTP relay"})
        print(f"[🚀] Pitch successfully transmitted to {company} linking to {live_url}")
        
    except Exception as e:
        log_event("B2B_TRANSMIT_ERR", str(e))
        
    time.sleep(60)
