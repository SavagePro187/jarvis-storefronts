#!/usr/bin/env python3
import sys
import os
import time
import urllib.request
import json
from jarvis_core_matrix import JarvisCoreMatrix
from jarvis_conglomerate import JarvisConglomerateEngine

def main_swarm_loop():
    matrix = JarvisCoreMatrix()
    conglomerate = JarvisConglomerateEngine()
    
    print("\n[*] Jarvis Master Swarm Coordinator Online.")
    print("========================================================")
    
    conglomerate.compile_all()
    
    worker_tasks = [
        {"name": "b2b_lead_scraper", "script": "b2b_lead_scraper.py"},
        {"name": "seo_tracker", "script": "seo_competitor_tracker.py"},
        {"name": "uptime_monitor", "script": "api_uptime_sla_monitor.py"},
        {"name": "leak_notifier", "script": "dark_web_leak_notifier.py"},
        {"name": "s3_finder", "script": "leaked_s3_bucket_finder.py"}
    ]
    
    print("\n[+] Enter instruction for Jarvis Core or type 'loop' to start continuous sub-agent tracking.")
    
    while True:
        try:
            user_input = input("\nsavage-jarvis 🤖 > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("[*] Shutting down swarm loops safely.")
                sys.exit(0)
                
            if user_input.lower() == "loop":
                print("[*] Entering Infinite Sub-Agent Execution Tracking Loop. Press Ctrl+C to break.")
                while True:
                    for task in worker_tasks:
                        print(f"\n[Tracking] Polling output state of sub-agent: {task['name']}")
                        if os.path.exists(task['script']):
                            output = matrix.execute_system_arm(f"python3 {task['script']}")
                            matrix.log_telemetry(f"SUB_AGENT_{task['name'].upper()}_EXEC", {"output": output[:200]})
                        time.sleep(3)
            else:
                print(f"Jarvis is analyzing directive string with qwen...")
                response = matrix.query_local_llm(user_input)
                print(f"\nJarvis: {response}")
                
                payload = {"global_directive": user_input[:50], "timestamp": int(time.time())}
                req = urllib.request.Request(
                    matrix.config["N8N_PRODUCTION_WEBHOOK"],
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"}
                )
                try:
                    with urllib.request.urlopen(req) as res:
                        matrix.dispatch_alert("n8n Production Gateway Webhook Telemetry Sync: OK")
                except Exception:
                    matrix.dispatch_alert("n8n Production Gateway Telemetry Sync: Offline/Skipped")
                    
        except KeyboardInterrupt:
            print("\n[*] Continuous execution loop paused. Returned to core shell wrapper.")
            continue
        except Exception as e:
            print(f"❌ Processing Error: {str(e)}")

if __name__ == "__main__":
    main_swarm_loop()
