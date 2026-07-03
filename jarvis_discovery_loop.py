#!/usr/bin/env python3
import json
import time
import sqlite3
import os
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
SEARXNG_ENDPOINT = "http://localhost:8080/search"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def execute_market_discovery():
    print("[+] Initiating Autonomous Market Discovery Sequence...")
    
    discovery_queries = [
        "fastest growing b2b software niches 2026",
        "highest margin digital agency business models",
        "booming high ticket e-commerce services"
    ]
    
    combined_metadata = []
    for q in discovery_queries:
        try:
            params = {"q": q, "format": "json"}
            res = requests.get(SEARXNG_ENDPOINT, params=params, timeout=15.0)
            if res.status_code == 200:
                results = res.json().get("results", [])
                for item in results[:3]:
                    combined_metadata.append(item.get("content", ""))
        except Exception:
            continue
            
    if not combined_metadata:
        print("[-] Market discovery search query pass returned empty datasets.")
        return

    raw_context = " ".join(combined_metadata)[:4000]
    
    ai_prompt = (
        f"Analyze this market metadata context: {raw_context}\n\n"
        "Identify exactly ONE highly profitable, trending digital business service model that can be automated via outreach. "
        "You must respond with exactly one clean JSON object and nothing else. No markdown wrappers, no backticks, no conversational text. "
        "The JSON structure must match this exact dictionary keys layout:\n"
        "{\n"
        "  \"operation_type\": \"UPPERCASE_SNAKE_CASE_SHORT_NAME\",\n"
        "  \"search_query_template\": \"\\\"Target Keyword\\\" query modifier mapping\",\n"
        "  \"target_email_prefix\": \"info or contact or hello\",\n"
        "  \"email_subject_template\": \"Catchy Subject Line - {comp}\",\n"
        "  \"llm_positioning_prompt\": \"Focus on a one-sentence B2B pitch value proposition targeting this specific niche business challenge.\"\n"
        "}"
    )

    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": ai_prompt,
        "stream": False,
        "options": {"num_ctx": 4096, "num_thread": 4, "num_predict": 512, "temperature": 0.3}
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300.0)
        raw_response = response.json().get("response", "").strip()
        
        if "```json" in raw_response:
            raw_response = raw_response.split("```json")[-1].split("```")[0].strip()
        elif "```" in raw_response:
            raw_response = raw_response.split("```")[-1].split("```")[0].strip()

        parsed_model = json.loads(raw_response)
        
        op_type = parsed_model.get("operation_type")
        query_tmpl = parsed_model.get("search_query_template")
        prefix = parsed_model.get("target_email_prefix")
        subj = parsed_model.get("email_subject_template")
        prompt = parsed_model.get("llm_positioning_prompt")
        
        if not all([op_type, query_tmpl, prefix, subj, prompt]):
            print("[-] AI generation payload was structurally incomplete.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM income_stream_registry WHERE operation_type = ?;", (op_type,))
        if cursor.fetchone():
            print(f"[~] Discovered income stream [{op_type}] already exists inside registry database.")
        else:
            cursor.execute("""
                INSERT INTO income_stream_registry (operation_type, search_query_template, target_email_prefix, email_subject_template, llm_positioning_prompt, is_active)
                VALUES (?, ?, ?, ?, ?, 1);
            """, (op_type, query_tmpl, prefix, subj, prompt))
            conn.commit()
            print(f"[🔥 REVENUE REVOLUTION] AI successfully discovered, verified, and registered a brand new digital income stream: [{op_type}]")
            
        conn.close()
        
    except Exception as err:
        print(f"[-] Discovery pipeline compilation anomaly: {err}")

if __name__ == "__main__":
    execute_market_discovery()
