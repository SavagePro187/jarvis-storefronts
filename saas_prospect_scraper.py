#!/usr/bin/env python3
import os
import sys
import json
import time
import sqlite3
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
SEARXNG_ENDPOINT = "http://localhost:8080/search"

def log_worker_data(niche, leads_found):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        payload = {"niche": niche, "leads_count": len(leads_found), "leads": leads_found, "status": "searxng_saas_filtered"}
        cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, timestamp, raw_payload) VALUES (?, ?, ?);", 
                       ("LEAD_SCRAPER_RUN_SUCCESS", int(time.time()), json.dumps(payload)))
        conn.commit()
        conn.close()
    except Exception as e:
        sys.exit(1)

def fetch_live_leads(niche):
    try:
        params = {"q": f'"{niche}" SaaS contact mail', "format": "json"}
        response = requests.get(SEARXNG_ENDPOINT, params=params, timeout=15.0)
        response.raise_for_status()
        results = response.json().get("results", [])
        
        extracted_leads = []
        for item in results[:2]:
            title = item.get("title", "Unknown SaaS")
            link = item.get("url", "")
            snippet = item.get("content", "")
            
            clean_name = title.split('-')[0].split('|')[0].split(':')[0].strip()
            domain = link.split('//')[-1].split('/')[0].replace("www.", "") if link else "target.io"
            
            if any(x in clean_name.lower() for x in ["top ", "best ", "list", "tools", "agencies", "hire", "companies", "2026"]) or len(clean_name) > 30:
                clean_name = domain.split('.')[0].capitalize()
            
            if any(bad in domain for bad in ["reddit.com", "quora.com", "github.com", "linkedin.com"]):
                continue
                
            extracted_leads.append({
                "company": clean_name,
                "target_email": f"contact@{domain}".lower(),
                "description": snippet[:100] + "..." if snippet else "SaaS infrastructure domain match."
            })
        return extracted_leads
    except Exception:
        return []

if __name__ == "__main__":
    target_niche = "AI Dev Tools"
    live_leads = fetch_live_leads(target_niche)
    if live_leads:
        log_worker_data(target_niche, live_leads)
        print(f"[SUCCESS] SaaS worker extracted {len(live_leads)} tech infrastructure nodes.")
    else:
        print("[!] SaaS worker returned zero new raw results.")
