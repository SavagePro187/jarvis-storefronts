#!/usr/bin/env python3
import os
import json
import sqlite3
import threading
import requests

DB_PATH = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
LOG_DIR = os.path.expanduser("~/.local/bin/agent_services/logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Define 3 highly specialized digital revenue niches
NIC_DESCRIPTIONS = {
    "api_arbitrage_broker": (
        "Write a Python 3 production script that continuously monitors free public APIs (like news, weather, or stocks) "
        "and structures, formats, and prepares them as a clean premium data product payload string. Log operations to SQLite."
    ),
    "pseo_funnel_builder": (
        "Write a Python 3 production script that programmatically reads high-velocity traffic keyword variations, "
        "generates simulated markdown landing pages with dynamic hooks, and saves customer interest intent arrays. Log operations to SQLite."
    ),
    "b2b_outreach_pipeline": (
        "Write a Python 3 production script that processes cold business validation matrices, structures personalized outbound "
        "transactional pitches, and saves clean draft arrays to a customer pipeline stack. Log operations to SQLite."
    )
}

def synthesize_and_deploy_agent(niche, strategy_prompt):
    print(f"[+] [THREAD ENGAGED] Starting parallel synthesis for: {niche}...")
    
    code_prompt = (
        f"Write a complete, working Python 3 production script that automates operations for this exact business asset: {strategy_prompt}.\n"
        f"The script must log periodic loop indicators to the SQLite database at {DB_PATH} inside table 'jarvis_business_logs' with columns (directive_executed, raw_payload).\n"
        "It must run continuously using an endless 'while True:' loop with a time.sleep(60) delay.\n"
        "Output ONLY functional Python code. Do not include markdown ticks, descriptions, notes, or structural wrappers."
    )

    try:
        res = requests.post("http://127.0.0.1:11434/api/generate", json={
            "model": "qwen2.5:1.5b",
            "prompt": code_prompt,
            "stream": False
        }, timeout=300)
        
        generated_code = res.json().get("response", "").strip()
        
        # Clean any accidental markdown code fences
        if "```" in generated_code:
            lines = generated_code.splitlines()
            cleaned_lines = [l for l in lines if not l.startswith("```")]
            generated_code = "\n".join(cleaned_lines)
            
    except Exception as e:
        print(f"[-] [THREAD FAILURE] AI code synthesis crashed for {niche}: {e}")
        return

    script_path = f"/Users/savage-p.c./Projects/active/jarvishive/agent_{niche}.py"
    with open(script_path, "w") as f:
        f.write(generated_code)
    print(f"[✔] [THREAD SUCCESS] Synthesized code file saved to {script_path}")

    # Launchctl Registration Phase
    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/com.user.agent_{niche}.plist")
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://apple.com">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.agent_{niche}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{LOG_DIR}/agent_{niche}_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{LOG_DIR}/agent_{niche}_stderr.log</string>
</dict>
</plist>
"""
    with open(plist_path, "w") as f:
        f.write(plist_content)

    os.system(f"launchctl unload {plist_path} 2>/dev/null")
    os.system(f"launchctl load {plist_path}")
    os.system(f"launchctl start com.user.agent_{niche}")
    print(f"[🚀] [DEPLOY COMPLETE] Agent com.user.agent_{niche} is fully online in background kernel space.")

def main():
    print("⚡ Launching Parallel Multi-Agent Deployment Routine Matrix via Qwen 2.5...")
    threads = []
    
    # Spawn a concurrent thread for each targeted agent model definition
    for niche, prompt in NIC_DESCRIPTIONS.items():
        t = threading.Thread(target=synthesize_and_deploy_agent, args=(niche, prompt))
        threads.append(t)
        t.start()

    # Hold main process block context until all threads finish running execution loops
    for t in threads:
        t.join()
        
    print("\n[✔] All 3 specialized agents have completed generation loops and are operating concurrently!")

if __name__ == "__main__":
    main()
