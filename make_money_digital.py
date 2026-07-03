#!/usr/bin/env python3
import os

WORKSPACE = "/Users/savage-p.c./Projects/active/jarvishive"

def build_digital_download_storefront(file_name, product_title, price_label, stripe_checkout_url):
    html_store = f"""<!DOCTYPE html>
<html>
<head><title>Get {product_title}</title><meta charset="utf-8"></head>
<body style="font-family:sans-serif; text-align:center; padding:50px; background:#f8fafc; color:#0f172a;">
    <h1 style="font-size:2.5em; margin-bottom:10px;">{product_title}</h1>
    <p style="color:#64748b; font-size:1.1em;">Download the complete production-ready open-source codebase template instantly.</p>
    <div style="margin:40px auto; max-width:450px; background:#fff; padding:40px; border-radius:12px; border:1px solid #e2e8f0; box-shadow:0 10px 15px -3px rgba(0,0,0,0.05);">
        <div style="font-size:3em; font-weight:bold; color:#0f172a; margin-bottom:20px;">{price_label}</div>
        <ul style="text-align:left; margin-bottom:30px; color:#334155; line-height:1.8;">
            <li>✔ Fully documented Python Master Orchestration module</li>
            <li>✔ Zero external paid software dependencies</li>
            <li>✔ Lifetime updates and structural schema patches</li>
        </ul>
        <a href="{stripe_checkout_url}" style="display:block; padding:18px; background:#0f172a; color:#fff; text-decoration:none; border-radius:6px; font-weight:bold; font-size:1.1em; transition:background 0.2s;">Buy and Download Instantly</a>
    </div>
</body>
</html>"""
    try:
        with open(os.path.join(WORKSPACE, file_name), "w") as f:
            f.write(html_store)
        print(f"[✔] Digital product storefront node deployed successfully: {file_name}")
        return True
    except Exception as e:
        print(f"[-] Deployment error: {e}")
        return False

if __name__ == "__main__":
    # Replace this link with your direct Stripe product checkout link
    MY_STRIPE_PRODUCT_LINK = "https://stripe.com"
    build_digital_download_storefront("digital_shop.html", "Jarvis Autonomous Workflow Boilerplate", "$29.00", MY_STRIPE_PRODUCT_LINK)
