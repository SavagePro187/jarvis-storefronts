#!/usr/bin/env python3
import os
import sys
import json
import time
import sqlite3
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
SEARXNG_ENDPOINT = "http://localhost:8080/search"

def run_universal_stream(op_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT search_query_template, target_email_prefix 
        FROM income_stream_registry 
        WHERE operation_type = ? AND is_active = 1;
    """, (op_type,))
    config = cursor.fetchone()
    
    if not config:
        conn.close()
        return False
        
    query, email_prefix = config
    
    try:
        params = {"q": query, "format": "json"}
        response = requests.get(SEARXNG_ENDPOINT, params=params, timeout=15.0)
        response.raise_for_status()
        results = response.json().get("results", [])
        
        extracted_leads = []
        for item in results[:3]:
            title = item.get("title", "Unknown Entity")
            link = item.get("url", "")
            snippet = item.get("content", "")
            
            clean_name = title.split('-')[0].split('|')[0].split(':')[0].strip()
            domain = link.split('//')[-1].split('/')[0].replace("www.", "") if link else "target.io"
            
            if any(x in clean_name.lower() for x in ["top ", "best ", "list", "tools", "agencies", "hire", "companies"]) or len(clean_name) > 30:
                clean_name = domain.split('.')[0].capitalize()
            
            if any(bad in domain for bad in ["reddit.com", "quora.com", "github.com", "linkedin.com"]):
                continue
                
            extracted_leads.append({
                "company": clean_name,
                "target_email": f"{email_prefix}@{domain}".lower(),
                "description": snippet[:100] + "..." if snippet else "Domain infrastructure matching operational profile."
            })
            
        if extracted_leads:
            payload = {"niche": op_type, "leads_count": len(extracted_leads), "leads": extracted_leads, "status": "searxng_universal_filtered"}
            cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, timestamp, raw_payload) VALUES (?, ?, ?);", 
                           ("LEAD_SCRAPER_RUN_SUCCESS", int(time.time()), json.dumps(payload)))
            conn.commit()
            print(f"[SUCCESS] [{op_type}] Universal worker captured {len(extracted_leads)} nodes.")
            
    except Exception as e:
        print(f"[-] Universal loop failure on {op_type}: {e}")
        
    conn.close()
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_universal_stream(sys.argv[1])
