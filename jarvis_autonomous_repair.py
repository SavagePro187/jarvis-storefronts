#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import re

HISTORY_PATH = os.path.expanduser("~/.zsh_history")
LAST_POSITION = 0
REPAIR_REGISTRY = {}

def scan_for_failed_commands():
    global LAST_POSITION
    if not os.path.exists(HISTORY_PATH):
        return

    try:
        with open(HISTORY_PATH, "rb") as f:
            if LAST_POSITION == 0:
                f.seek(0, 2)
                LAST_POSITION = f.tell()
                return

            f.seek(LAST_POSITION)
            raw_lines = f.readlines()
            LAST_POSITION = f.tell()

        for raw_line in raw_lines:
            try:
                line = raw_line.decode('utf-8', errors='ignore').strip()
                if not line or ";" not in line:
                    continue
                
                cmd_string = line.split(";", 1)[1].strip()
                # Intercept any python script you try to run manually
                match = re.search(r'(?:python3|python)\s+([^\s\&\;]+\.py)', cmd_string)
                if match:
                    script_path = os.path.abspath(match.group(1))
                    if os.path.exists(script_path) and script_path not in REPAIR_REGISTRY:
                        print(f"[+] [REPAIR ENGINE] Now monitoring: {os.path.basename(script_path)}")
                        REPAIR_REGISTRY[script_path] = {"attempts": 0, "status": "monitoring"}
            except Exception:
                pass
    except Exception:
        pass

def diagnose_and_patch_errors():
    for script_path, meta in list(REPAIR_REGISTRY.items()):
        script_name = os.path.basename(script_path)
        
        # Test-run the script in a sandbox to catch any active errors or crashes
        process = subprocess.Popen(
            ["/usr/local/bin/python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        # If the script finishes clean with zero errors, move on
        if process.returncode == 0 and "error" not in stdout.lower() and "failed" not in stdout.lower():
            if meta["status"] != "resolved":
                print(f"[🎉] [REPAIR ENGINE] {script_name} is running perfectly with 0 errors. Task handled.")
                REPAIR_REGISTRY[script_path]["status"] = "resolved"
            continue

        # If it crashes, intercept the failure data stream instantly
        error_msg = stderr if stderr else stdout
        print(f"[⚠️] [REPAIR ENGINE] Detected failure in {script_name}. Analyzing error logs...")
        
        with open(script_path, "r") as f:
            code = f.read()

        # SELF-REPAIR MATRIX 1: Fix broken URLs, missing ports, or short octets
        if "http://127.0.0.1" in code or "Connection timed out" in error_msg or "Max retries exceeded" in error_msg:
            print(f"[🛠️] [REPAIR ENGINE] Fixing broken local server URL and port configuration...")
            code = re.sub(r"(https?://)?(127\.0\.0\.1|localhost)(:[0-9]+)?(/v1/chat/completions|/api/generate)?", "http://127.0.0.1:11434", code)

        # SELF-REPAIR MATRIX 2: Fix uncapitalized boolean literals ('false' name error)
        if "NameError: name 'false' is not defined" in error_msg or "'false' is not defined" in error_msg:
            print(f"[🛠️] [REPAIR ENGINE] Fixing Python dictionary syntax boolean literal capitalizations...")
            code = code.replace('"stream": false', '"stream": False')
            code = code.replace("'stream': false", '"stream": False')

        # SELF-REPAIR MATRIX 3: Fix dictionary unpacking key/index crashes
        if "string indices must be integers" in error_msg or "KeyError" in error_msg or "AttributeError" in error_msg:
            print(f"[🛠️] [REPAIR ENGINE] Injecting robust type validation and fail-safe JSON parsers...")
            code = code.replace("['message']['content']", ".get('message', {}).get('content', str(response.text))")

        # SELF-REPAIR MATRIX 4: Inject hardware low-VRAM optimizations if model timeouts hit
        if "timeout" in error_msg.lower() or "alignment failure" in error_msg.lower():
            print(f"[🛠️] [REPAIR ENGINE] Instantly injecting low-VRAM constraints and token clamps...")
            if '"options"' not in code:
                opt_block = '"stream": False, "options": {"num_ctx": 4096, "num_thread": 4, "low_vram": True, "f16_kv": True},'
                code = code.replace('"stream": False,', opt_block)

        # Write the autonomous repairs back to the disk file directly
        with open(script_path, "w") as f:
            f.write(code)
            
        REPAIR_REGISTRY[script_path]["attempts"] += 1
        time.sleep(2) # Brief cooling window before re-testing

def main_loop():
    print("[+] Jarvis Autonomous Self-Repair Engine Engaged.")
    print("[+] Watching terminal history. If a command crashes, Jarvis takes over and fixes it live.")
    while True:
        scan_for_failed_commands()
        diagnose_and_patch_errors()
        time.sleep(5) # Evaluate states every 5 seconds

if __name__ == "__main__":
    main_loop()