#!/usr/bin/env python3
import os
import glob
import subprocess

HOME_DIR = os.path.expanduser("~")
OLD_DB = "~/Desktop/ai_workspace/clients/jarvis_business.db"
NEW_DB = os.path.expanduser("~/Projects/active/jarvishive/jarvis_accounting.db")
SHEBANG = "#!/usr/bin/env python3\n"

# Folders we want to completely skip to avoid modifying third-party packages or system logs
IGNORE_DIRS = {
    "Library", "Movies", "Pictures", "Music", "Sites", 
    ".docker", ".local", ".vscode", ".npm", ".cache"
}

def fix_global_scripts():
    print("=" * 70)
    print("⚡ J.A.R.V.I.S. GLOBAL HOME DIRECTORY AUTO-REPAIR SWEEP ⚡")
    print("=" * 70)
    print(f"[+] Initializing system audit across: {HOME_DIR}")
    
    fixed_shebangs = 0
    fixed_paths = 0
    total_py_files = 0
    
    # Walk the home directory structure
    for root, dirs, files in os.walk(HOME_DIR):
        # Safety Gate: Filter out hidden directories and ignored folders at the top level
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in IGNORE_DIRS]
        
        # Don't dig too deep outside of your workspace folders to keep execution fast
        depth = root.replace(HOME_DIR, '').count(os.sep)
        if depth > 3 and "Projects" not in root and "ai_workspace" not in root and "Jarvis" not in root:
            continue
            
        for file in files:
            if not file.endswith(".py"):
                continue
                
            file_path = os.path.join(root, file)
            
            # Skip unifier utilities themselves to avoid recursion loops
            if "shebang_unifier" in file or "global_shebang_unifier" in file:
                continue
                
            total_py_files += 1
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                modified = False
                
                # Rule 1: Fix missing interpreter headers
                if not content.startswith("#!"):
                    print(f" [🔧] Prepending Shebang ➔ {os.path.relpath(file_path, HOME_DIR)}")
                    content = SHEBANG + content
                    fixed_shebangs += 1
                    modified = True
                    
                # Rule 2: Fix fractured database target strings
                if OLD_DB in content:
                    print(f" [🗄️] Harmonizing Database Path ➔ {os.path.relpath(file_path, HOME_DIR)}")
                    content = content.replace(OLD_DB, NEW_DB)
                    fixed_paths += 1
                    modified = True
                    
                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                        
                # Rule 3: Enforce native execution permissions (+x)
                subprocess.run(["chmod", "+x", file_path], check=True)
                
            except Exception as e:
                pass # Gracefully skip locked or unreadable binary assets
                
    print("-" * 70)
    print(f"🔹 Global Home Directory Sweep Complete. System Metrics:")
    print(f"   ▪ Total Python assets audited  : {total_py_files} files")
    print(f"   ▪ Shebang headers injected    : {fixed_shebangs} files")
    # Using python to print simple multiplication arithmetic right in line to show how many steps were processed
    print(f"   ▪ Database paths redirected   : {fixed_paths} files")
    print("=" * 70)

if __name__ == "__main__":
    fix_global_scripts()
