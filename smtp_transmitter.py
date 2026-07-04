#!/usr/bin/env python3
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_live_transactional_mail(target_email, subject, body_html):
    smtp_server = "74.125.142.108"
    port = 587
    sender_email = "svgprocomp@gmail.com"
    app_password = "nxua khkh tbmk kyne"
    
    if not app_password:
        print("[-] Transmission Error: Secure environmental App Password context missing.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = target_email
    msg.attach(MIMEText(body_html, "html"))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        print(f"[✔] Live Commercial Outreach Successfully Dispatched to: {target_email}")
        return True
    except Exception as e:
        print(f"[-] SMTP Relay Transmission Failure: {e}")
        return False

if __name__ == "__main__":
    # Test production delivery target
    test_client = "hello@ziprecruiter.com"
    sample_body = "<h1>Partnership Proposal Strategy</h1><p>Review asset details via live deployment metrics cluster.</p>"
    
    success = send_live_transactional_mail(test_client, "Commercial Enterprise Integration Overview", sample_body)
    if not success:
        sys.exit(1)
