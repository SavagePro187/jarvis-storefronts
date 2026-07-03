#!/usr/bin/env python3
import requests
import json
import sqlite3
import os

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")

def discover_opportunities():
    # Target high-velocity digital arbitrage sectors
    # E.g., Open API documentation, trending micro-SaaS GitHub boilerplates, digital ad-spend fluctuations
    data_sources = [
        "https://hnrss.org",
        "https://github.com:>2026-06-01&sort=stars&order=desc"
    ]
    raw_payloads = []
    for url in data_sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                raw_payloads.append(res.text[:5000]) # Sample data blocks
        except Exception:
            continue

    # Feed raw data into Llama 3 to output highly specific digital income opportunities
    prompt = f"Analyze these raw market trend datasets: {str(raw_payloads)}. Identify a single monetization opportunity that can be built via automated script engines. Output JSON format only: {{'niche': 'string', 'strategy': 'string', 'required_files': ['string']}}"
    
    ollama_res = requests.post("http://127.0.0.1:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }, timeout=300)
    
    opportunity = json.loads(ollama_res.json().get("response", "{}"))
    return opportunity

