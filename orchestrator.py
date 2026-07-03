#!/usr/bin/env python3
import subprocess
import os
import sys
import time

# Define the sequence of scripts you want to actually run
CYCLE_SEQUENCE = [
    "./tool_key_scanner.py",
    "./parse_incoming_intents.py",
    "./tool_live_publisher.py",
    "./smtp_transmitter.py",
    "./b2b_lead_scraper.py",
    "./tool_storefront_builder.py"
]

def print_banner(text):
    print("=" * 56)
    print(f"[*] {text}")
    print("=" * 56)

def execute_script(script_path):
    # Verify file exists before trying to run it
    if not os.path.exists(script_path):
        print(f"[❌] Error: File {script_path} does not exist!")
        return False

    print(f"[Jarvis Strategic Move]: Target: jarvishive -> Executing: '{script_path}'")
    
    try:
        # This line actually runs the file on your machine
        # it streams the stdout/stderr directly to your terminal screen
        process = subprocess.Popen(
            [script_path],
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        
        # Wait for the script to finish running
        exit_code = process.wait()
        
        if exit_code == 0:
            print(f"[✔] Action committed successfully: {script_path}\n")
            return True
        else:
            print(f"[❌] Action failed: {script_path} exited with code {exit_code}\n")
            return False
            
    except PermissionError:
        print(f"[❌] Permission Denied: You must run 'chmod +x {script_path}' in terminal.\n")
        return False
    except Exception as e:
        print(f"[❌] Unexpected system error executing {script_path}: {e}\n")
        return False

def main():
    print_banner("Jarvis High-Velocity Commercial Cycle Engaged")
    
    for script in CYCLE_SEQUENCE:
        success = execute_script(script)
        if not success:
            print("[⚠️] Cycle interrupted due to an error. Halting loop.")
            break
        time.sleep(1) # Brief pause between tasks

if __name__ == "__main__":
    main()

