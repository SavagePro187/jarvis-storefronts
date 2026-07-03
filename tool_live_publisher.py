#!/usr/bin/env python3
import os
import sys
import subprocess

WORKSPACE = "/Users/savage-p.c./Projects/active/jarvishive"

def publish_to_free_github_pages(file_name):
    # This automatically tracks changes, commits them locally, and forces an automated cloud deploy
    try:
        # Check if Git is initialized in the workspace directory
        if not os.path.exists(os.path.join(WORKSPACE, ".git")):
            subprocess.run("/usr/bin/git init", shell=True, cwd=WORKSPACE, check=True)
            subprocess.run("/usr/bin/git checkout -b main", shell=True, cwd=WORKSPACE, check=True)
            print("[+] Initialized local free Git asset pipeline.")

        # Stage file, commit changes, and sync out
        subprocess.run("/usr/bin/git add .", shell=True, cwd=WORKSPACE, check=True)
        
        # Check if there are active modifications before compiling a tree commit
        status = subprocess.run("git diff-index --quiet HEAD --", shell=True, cwd=WORKSPACE)
        if status.returncode != 0:
            subprocess.run('git commit -m "Autonomous edge site update Deployment cycle"', shell=True, cwd=WORKSPACE, check=True)
            subprocess.run("/usr/bin/git push -u origin main --force", shell=True, cwd=WORKSPACE, check=True)
        
        # Read the current origin remote string to layout your free public rendering link URL
        remote_res = subprocess.run("/usr/bin/git remote get-url origin", shell=True, cwd=WORKSPACE, capture_output=True, text=True)
        if remote_res.returncode == 0:
            # Parse your git path context to display your actual free public web URL link layout
            git_url = remote_res.stdout.strip().replace("git@github.com:", "").replace("https://github.com", "")
            user, repo = git_url.replace(".git", "").split("/")
            public_url = f"https://{user}.github.io/{repo}/{file_name}"
            print(f"[🚀] LIVE DEPLOYMENT DEPLOYED TO FREE EDGE HOSTING -> {public_url}")
        else:
            print("[⚠️] Sync Complete. Link warning: Connect this folder to a free GitHub repository remote via: git remote add origin <url>")
        return True
    except Exception as e:
        print(f"[-] Free Distribution Matrix Failure: {e}")
        return False

if __name__ == "__main__":
    target_resource = "shop_premium_lead_engine.html"
    if publish_to_free_github_pages(target_resource):
        print("[SUCCESS] Free static web edge-network orchestration complete.")
    else:
        sys.exit(1)
