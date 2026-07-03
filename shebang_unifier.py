#!/usr/bin/env python3
import os
import glob
import subprocess

TARGET_DIR = os.path.expanduser("~/Projects/active/jarvishive")
OLD_DB = "~/Desktop/ai_workspace/clients/jarvis_business.db"
NEW_DB = "~/Projects/active/jarvishive/jarvis_accounting.db"
SHEBANG = "#!/usr/bin/env python3\n"

def fix_all_scripts():
    print("=" * 60)
    print("⚡ J.A.R.V.I.S. AUTO-REPAIR & SYSTEM SHEBANG UNIFIER ⚡")
    print("=" * 60)
    
    # Locate all python files in the target path
    search_path = os.path.join(TARGET_DIR, "*.py")
    py_files = glob.glob(search_path)
    
    fixed_shebangs = 0
    fixed_paths = 0
    
    for file_path in py_files:
        # Skip this utility script itself
        if "shebang_unifier.py" in file_path:
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            modified = False
            
            # Fix 1: Check and prepend missing shebang line
            if not content.startswith("#!"):
                print(f" [🔧] Missing shebang detected ➔ Fixing: {os.path.basename(file_path)}")
                content = SHEBANG + content
                fixed_shebangs += 1
                modified = True
                
            # Fix 2: Check and fix legacy database path strings
            if OLD_DB in content:
                print(f" [🗄️] Legacy database string path detected ➔ Redirecting: {os.path.basename(file_path)}")
                content = content.replace(OLD_DB, NEW_DB)
                fixed_paths += 1
                modified = True
                
            # Write modifications back to disk safely if changes occurred
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
            # Fix 3: Grant universal execution permissions (+x) natively
            subprocess.run(["chmod", "+x", file_path], check=True)
            
        except Exception as e:
            print(f" [❌] Error accessing asset {os.path.basename(file_path)}: {e}")
            
    print("-" * 60)
    print(f"🔹 Execution Sweep Complete. Result Matrix Summary:")
    print(f"   ▪ Shebang headers injected : {fixed_shebangs} scripts")
    print(f"   ▪ Database paths redirected: {fixed_paths} scripts")
    print(f"   ▪ Executable rules applied : {len(py_files) - 1} scripts")
    print("=" * 60)

if __name__ == "__main__":
    fix_all_scripts()
