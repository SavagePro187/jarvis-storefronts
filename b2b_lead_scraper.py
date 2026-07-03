#!/usr/bin/env python3
import os
import sys
import json
import time
import sqlite3
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
SEARXNG_ENDPOINT = "http://127.0.0.1:8080"

def log_worker_data(niche, leads_found):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jarvis_business_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                directive_executed TEXT NOT NULL, 
                timestamp INTEGER NOT NULL, 
                raw_payload TEXT NOT NULL
            );
        """)
        payload = {"niche": niche, "leads_count": len(leads_found), "leads": leads_found, "status": "searxng_business_filtered"}
        cursor.execute("INSERT INTO jarvis_business_logs (directive_executed, timestamp, raw_payload) VALUES (?, ?, ?);", 
                       ("LEAD_SCRAPER_RUN_SUCCESS", int(time.time()), json.dumps(payload)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Worker DB logging failure: {e}")

def fetch_live_leads(niche):
    print(f"[+] Querying local SearXNG instance with strict commercial filtering blocks...")
    
    # Advanced search string targeting direct business products while dropping content blogs
    filtered_query = f'"{niche}" (site:.com OR site:.io) -inurl:blog -inurl:article -inurl:best -inurl:review -inurl:top -intitle:best -intitle:top -intitle:review'
    
    params = {
        "q": filtered_query,
        "format": "json",
        "engines": "google,bing,duckduckgo",
        "language": "en-US"
    }
    
    try:
        response = requests.get(SEARXNG_ENDPOINT, params=params, timeout=15.0)
        response.raise_for_status()
        search_data = response.json()
        results = search_data.get("results", [])
        
        if results:
            extracted_leads = []
            for item in results[:3]:
                title = item.get("title", "Unknown Corporation")
                link = item.get("url", "")
                snippet = item.get("content", "")
                
                # Advanced structural title cleaning
                clean_name = title.split('-')[0].split('|')[0].split(':')[0].split('—')[0].strip()
                
                # Strip typical listicle noise words
                for noise in ['Free ', 'Best ', 'Top ', 'Review', 'Platform', 'Tool', 'Software', 'Compared']:
                    clean_name = clean_name.replace(noise, '').strip()
                
                # Re-derive domain early for fallback structural safety
                domain = link.split('//')[-1].split('/')[0].replace('www.', '') if link else 'target.io'
                
                # If clean_name is still a long sentence or blog artifact, extract clean brand name from domain
                if len(clean_name.split()) > 3 or len(clean_name) > 25:
                    clean_name = domain.split('.')[0].capitalize()
                domain = link.split("//")[-1].split("/")[0].replace("www.", "") if link else "target.io"
                
                # Protect database from bad informational/forum nodes
                blocklist = ["reddit.com", "quora.com", "medium.com", "github.com", "linkedin.com", "youtube.com"]
                if any(bad in domain for bad in blocklist):
                    continue
                    
                extracted_leads.append({
                    "company": clean_name,
                    "target_email": f"info@{domain}".lower(),
                    "description": snippet[:100] + "..." if snippet else "No description metadata discovered."
                })
            return extracted_leads
    except Exception as e:
        print(f"[!] Scraper query route interrupted: {e}")
        sys.exit(1)
        
    print("[!] Local SearXNG instance returned zero raw query results.")
    sys.exit(1)

def main():
    print("[+] Initializing Advanced Business Target Scraper Worker Pipeline...")
    target_niche = "free email marketing platform"
    
    live_leads = fetch_live_leads(target_niche)
    log_worker_data(target_niche, live_leads)
    print(f"[SUCCESS] Worker extracted {len(live_leads)} direct business corporate nodes.")
    sys.exit(0)

if __name__ == "__main__":
    main()
