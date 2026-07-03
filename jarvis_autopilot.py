#!/usr/bin/env python3
import os
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "local-bypass"
import subprocess
import os
import sys

def execute_with_auto_heal(command, cwd=None):
    """Executes a command. If a known environment error occurs, Jarvis heals it automatically."""
    print(f"🤖 Jarvis executing: {command}")
    
    # Run the initial process injection
    process = subprocess.run(
        command, shell=True, capture_output=True, text=True, cwd=cwd
    )
    
    # Check for the exact virtual environment module error you just hit
    if process.returncode != 0 and "ModuleNotFoundError" in process.stderr:
        print("⚠️ Jarvis detected missing environment modules. Initiating Auto-Heal sequence...")
        
        venv_activate = os.path.join(cwd if cwd else "", "venv/bin/activate")
        
        # Self-Correction Step 1: Ensure virtual environment exists
        if not os.path.exists(os.path.dirname(venv_activate)):
            print("🔧 Creating missing Python virtual environment workspace...")
            subprocess.run("python3 -m venv venv", shell=True, cwd=cwd)
            
        # Self-Correction Step 2: Auto-install broken or missing framework dependencies
        print("🔧 Injecting required API framework modules into the sandbox...")
        subprocess.run("./venv/bin/pip install fastapi uvicorn pydantic", shell=True, cwd=cwd)
        
        # Self-Correction Step 3: Automatically retry the execution inside the correct path
        print("🔄 Re-executing original target process...")
        healed_process = subprocess.run("./venv/bin/python3 jarvis_arms.py", shell=True, cwd=cwd)
        return healed_process
        
    if process.returncode != 0:
        print(f"❌ Execution failed:\n{process.stderr}")
    else:
        print(f"✅ Success:\n{process.stdout}")
    return process

if __name__ == "__main__":
    # Commands Jarvis to launch jarvis_arms.py while auto-managing its own dependencies
    execute_with_auto_heal("python3 jarvis_arms.py", cwd="/Users/savage-p.c./Projects/active/jarvishive")
