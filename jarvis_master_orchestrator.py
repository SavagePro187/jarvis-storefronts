#!/usr/bin/env python3
import json
import time
import sqlite3
import subprocess
import sys
import os
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
COMPANY_NAME = "SAVAGE PRODUCTION COMPANY LLC"
POSTAL_ADDRESS = "1433 BIRCH STREET, MONTEBELLO, CA 90640"

def get_clean_footer(target_email):
    return "\n\n---\nThis is a commercial communication from " + COMPANY_NAME + ".\nPostal Address: " + POSTAL_ADDRESS + "\nIf you wish to stop receiving corporate scaling indicators, reply with \x27REMOVE\x27 or click here to opt out: mailto:svgprocomp@://gmail.com" + target_email + "%20from%20your%20corporate%20scaling%20indicators."

def query_inference_engine(company_name, metadata, positioning_prompt):
    clean_prompt = "Write a sharp, high-converting ONE-SENTENCE B2B pitch opener from " + COMPANY_NAME + " to the company \"" + company_name + "\".\nContext about them: " + str(metadata) + ".\nPositioning objective: " + str(positioning_prompt) + "\n\nSTRICT RULES:\n1. Output exactly ONE short sentence. Do not write a paragraph.\n2. Do NOT include greeting phrases, subject lines, signature blocks, or text placeholders.\n3. Speak directly to their value proposition. Do NOT invent locations or financial metrics.\n4. Your output must end immediately after the first punctuation mark."
    payload = {
        "model": "qwen2.5:3b" if "GEN" in positioning_prompt or "PITCH" in positioning_prompt else "llama3:8b",
        "prompt": clean_prompt,
        "stream": False,
        "options": {"num_ctx": 2048, "num_thread": 4, "num_predict": 45, "low_vram": True, "temperature": 0.2}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=5.0)
        if "application/json" in response.headers.get("Content-Type", ""):
            content = response.json().get("response")
            if content and content.strip():
                return content.strip().strip('"\x27').strip('"\x27')
    except:
        pass
    return "Let us scale your business workflow."

def init_database_safely(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS income_stream_registry (id INTEGER PRIMARY KEY AUTOINCREMENT, operation_type TEXT UNIQUE, llm_positioning_prompt TEXT, is_active INTEGER DEFAULT 0);")
    cursor.execute("CREATE TABLE IF NOT EXISTS jarvis_business_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, directive_executed TEXT, raw_payload TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS global_suppression_list (email TEXT UNIQUE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS outbound_pitch_staging (id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, target_email TEXT UNIQUE, customized_pitch TEXT, generation_timestamp INTEGER, operation_type TEXT, worker_id TEXT);")
    conn.commit()

def process_active_streams():
    conn = sqlite3.connect(DB_PATH)
    init_database_safely(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT operation_type, llm_positioning_prompt FROM income_stream_registry WHERE is_active = 1;")
    streams = cursor.fetchall()
    if not streams:
        conn.close()
        return
    for stream in streams:
        op_type, positioning_prompt = stream
        print(f"\n[+] Executing Dynamic Stream -> [{op_type}]")
        worker_path = os.path.expanduser("~/Projects/active/jarvishive/universal_worker.py")
        if os.path.exists(worker_path):
            subprocess.run([sys.executable, worker_path, op_type])
        cursor.execute("SELECT raw_payload FROM jarvis_business_logs WHERE directive_executed = \x27LEAD_SCRAPER_RUN_SUCCESS\x27 AND raw_payload LIKE ? ORDER BY id DESC LIMIT 1;", (f"%{op_type}%",))
        row = cursor.fetchone()
        if not row: continue
        try: leads = json.loads(row[0]).get("leads", [])
        except: continue
        print(f" [~] Processing {len(leads)} scraped records for target conversion...")
        for lead in leads:
            comp = lead.get("company", "").capitalize()
            email = lead.get("target_email")
            meta = lead.get("description")
            if not email or "@" not in email: continue
            cursor.execute("SELECT 1 FROM global_suppression_list WHERE email = ?;", (email,))
            if cursor.fetchone(): continue
            pitch_body = query_inference_engine(comp, meta, positioning_prompt)
            final_pitch = f"{pitch_body}{get_clean_footer(email)}\n\nThis communication was tailored to your domain configuration."
            try:
                cursor.execute("INSERT INTO outbound_pitch_staging (company_name, target_email, customized_pitch, generation_timestamp, operation_type, worker_id) VALUES (?, ?, ?, ?, ?, \x27universal_worker.py\x27);", (comp, email, final_pitch, int(time.time()), op_type))
                print(f" [STAGED] Staged personalized outbound vector for {comp} ({email})")
            except sqlite3.IntegrityError: pass
        conn.commit()
    conn.close()

if __name__ == "__main__":
    print("[=== JARVIS DYNAMIC ENGINE MULTI-STREAM START ===]")
    process_active_streams()
    try:
        from pipeline_verification_engine import run_eol_verification
        print("\n[+] Launching pipeline verification routine...")
        run_eol_verification()
    except ImportError: pass
