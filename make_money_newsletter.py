#!/usr/bin/env python3
import os
import json

WORKSPACE = "/Users/savage-p.c./Projects/active/jarvishive"

def compile_premium_newsletter_issue(file_name, industry_niche, stripe_subscription_url):
    brief_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:sans-serif; line-height:1.6; max-width:600px; margin:0 auto; padding:20px; color:#222;">
    <div style="background:#0f172a; color:#fff; padding:20px; text-align:center; border-radius:5px 5px 0 0;">
        <h2>The Alpha Network: {industry_niche} Operations Brief</h2>
    </div>
    <div style="padding:20px; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 5px 5px;">
        <p>Greetings Operational Partner,</p>
        <p>This cycle's automation telemetry indicates heavy structural growth scaling across B2B lead generation sectors. Businesses utilizing localized open-source model pipelines are achieving up to a 40% reduction in customer acquisition latencies.</p>
        <hr style="border:none; border-top:1px solid #e2e8f0; margin:20px 0;">
        <p style="font-size:0.9em; color:#475569;">You are receiving the free summary edition. To unlock full technical pipeline schematics and real-time lead analytics data logs, upgrade to our premium tier instantly.</p>
        <div style="text-align:center; margin:30px 0;">
            <a href="{stripe_subscription_url}" style="display:inline-block; padding:15px 30px; background:#10b981; color:#fff; text-decoration:none; border-radius:5px; font-weight:bold;">Upgrade to Premium Briefs ($19/mo)</a>
        </div>
    </div>
</body>
</html>"""
    try:
        with open(os.path.join(WORKSPACE, file_name), "w") as f:
            f.write(brief_content)
        print(f"[✔] Monetized premium email copy brief generated successfully: {file_name}")
        return True
    except Exception as e:
        print(f"[-] File write error: {e}")
        return False

if __name__ == "__main__":
    # Replace this link with a Stripe Customer Portal Subscription Link (100% free to set up upfront)
    MY_STRIPE_SUBSCRIPTION_LINK = "https://stripe.com"
    compile_premium_newsletter_issue("premium_brief_template.html", "Digital Marketing Analytics", MY_STRIPE_SUBSCRIPTION_LINK)
