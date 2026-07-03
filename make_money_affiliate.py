#!/usr/bin/env python3
import os

WORKSPACE = "/Users/savage-p.c./Projects/active/jarvishive"

def build_free_affiliate_portal(file_name, niche, raw_affiliate_url):
    html_layout = f"""<!DOCTYPE html>
<html>
<head><title>Top Recommended {niche} Resources</title><meta charset="utf-8"></head>
<body style="font-family:sans-serif; text-align:center; padding:50px; background:#fafafa; color:#333;">
    <h1 style="color:#1d4ed8;">Exclusive {niche} Tools & Recommendations</h1>
    <p>Hand-picked enterprise-grade infrastructure assets deployed for optimizing production pipelines.</p>
    <div style="margin:50px auto; max-width:400px; padding:30px; background:#fff; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
        <h3>Premium Network Node Stack</h3>
        <p style="color:#666; font-size:0.9em;">Deploy your architecture across global edge systems with maximized throughput velocities.</p>
        <a href="{raw_affiliate_url}" style="display:inline-block; margin-top:20px; padding:15px 30px; background:#1d4ed8; color:#fff; text-decoration:none; border-radius:5px; font-weight:bold;">Access Resource Workspace</a>
    </div>
</body>
</html>"""
    try:
        with open(os.path.join(WORKSPACE, file_name), "w") as f:
            f.write(html_layout)
        print(f"[✔] Affiliate storefront matrix compiled: {file_name}")
        return True
    except Exception as e:
        print(f"[-] Compilation error: {e}")
        return False

if __name__ == "__main__":
    # Swap out this placeholder URL with your actual free affiliate link from Amazon, ClickBank, or Impact
    MY_FREE_AFFILIATE_LINK = "https://clickbank.net"
    build_free_affiliate_portal("affiliate_portal.html", "Cloud Infrastructure Hosting", MY_FREE_AFFILIATE_LINK)
