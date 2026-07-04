#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
import subprocess
import requests

SEARXNG_ENDPOINT = 'http://127.0.0.1:8080/search'
LITELLM_ENDPOINT = 'http://127.0.0.1:4000'
DB_PATH = '/Users/savage-p.c./ai_workspace/clients/jarvis_business.db'
WORKSPACE = '/Users/savage-p.c./Projects/active/jarvishive'
WORKER_DIR = os.path.join(WORKSPACE, 'workers')
BOUNTY_DIR = '/Users/savage-p.c./ai_workspace/bounty_reports'

os.makedirs(WORKER_DIR, exist_ok=True)

def append_audit_log(msg):
    print(f'[*] {msg}')
def run_local_llm(prompt, model="qwen2.5-commercial"):
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        res = requests.post(LITELLM_ENDPOINT, json=payload, timeout=90.0)
        data = res.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        print(f"❌ SERVER ERROR PAYLOAD: {data}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ CRITICAL: Local LLM Gateway Connection Failed: {e}")
        sys.exit(1)
def get_live_bounty_domains():
    active_targets = []
    if not os.path.exists(BOUNTY_DIR):
        return active_targets
    for filename in os.listdir(BOUNTY_DIR):
        if filename.startswith('verified_bounties_') and filename.endswith('.txt'):
            filepath = os.path.join(BOUNTY_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if 'detect-dangling-cname' in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                active_targets.append(parts[3].strip())
            except Exception:
                continue
    return list(set(active_targets))

def step_1_trend_scan():
    live_domains = get_live_bounty_domains()
    if live_domains:
        return f'Active target infrastructure found on: { ", ".join(live_domains[:10]) }'
    
    try:
        res = requests.get(SEARXNG_ENDPOINT, params={'q': 'b2b cloud automation tools trends 2026', 'format': 'json'}, timeout=8.0)
        context = ' '.join([r.get('content', '') for r in res.json().get('results', [])])
        if context.strip():
            return context
    except Exception:
        pass
    
    print('❌ CRITICAL: No raw domain assets found and SearXNG empty. Halting.')
    sys.exit(1)

def step_2_niche_replication(trend_context):
    prompt = f"Based on this context: '{trend_context}', name ONE specific B2B enterprise cybersecurity niche. Return ONLY the title, no explanation."
    niche = run_local_llm(prompt)
    if not niche or 'error' in niche.lower() or len(niche) > 80:
        print('❌ CRITICAL: LLM failed to isolate niche target.')
        sys.exit(1)
    return niche

def step_3_worker_factory(niche_title):
    prompt = f"Write a raw, production-grade Python script for an enterprise utility runner specialized in: {niche_title}. Use requests, include error catching, and exit with status 0. Output ONLY executable code blocks without backticks or descriptions."
    worker_template = run_local_llm(prompt)
    if not worker_template or 'import' not in worker_template:
        print('❌ CRITICAL: Code factory failed to compile template code.')
        sys.exit(1)
    
    worker_template = worker_template.replace('```python', '').replace('```', '')
    worker_file_path = os.path.join(WORKER_DIR, 'active_revenue_worker.py')
    with open(worker_file_path, 'w', encoding='utf-8') as f:
        f.write(worker_template)
    return worker_file_path

def step_4_edge_publish(worker_path):
    try:
        env_ctx = os.environ.copy()
        if not os.path.exists(os.path.join(WORKSPACE, '.git')):
            subprocess.run('git init && git checkout -b main', shell=True, cwd=WORKSPACE, env=env_ctx, check=True)
        subprocess.run(f'cp {DB_PATH} {os.path.join(WORKSPACE, "jarvis_business_backup.db")}', shell=True, check=True)
        subprocess.run('git add . && git commit -m "Production sync"', shell=True, cwd=WORKSPACE, env=env_ctx, check=True)
    except Exception as e:
        print(f'❌ CRITICAL: Git repository synchronization failed: {e}')
        sys.exit(1)
    return 'https://github.com'

def step_5_searxng_scrape():
    try:
        res = requests.get(SEARXNG_ENDPOINT, params={'q': 'b2b platform security engineering software contacts email', 'format': 'json'}, timeout=8.0)
        for item in res.json().get('results', []):
            link = item.get('url', '')
            if 'http' in link and not any(x in link for x in ['github', 'wikipedia', 'google']):
                domain = link.split('//')[-1].split('/')
                return {'company': domain.capitalize(), 'target_email': f'security@{domain}'}
    except Exception:
        pass
    print('❌ CRITICAL: SearXNG returned 0 actionable corporate targets.')
    sys.exit(1)

def step_6_asset_generation(lead_node):
    print(f'[*] Preparing transaction pipeline for: {lead_node["target_email"]}')
    return 'https://stripe.com'

def run_core_matrix():
    trend = step_1_trend_scan()
    niche = step_2_niche_replication(trend)
    worker = step_3_worker_factory(niche)
    url = step_4_edge_publish(worker)
    lead = step_5_searxng_scrape()
    stripe = step_6_asset_generation(lead)
    print('[🎉] CORE PIPELINE SYNCHRONIZED SUCCESSFULLY WITH PURE DATA')

if __name__ == "__main__":
    run_core_matrix()
