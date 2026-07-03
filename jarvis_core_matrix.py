#!/usr/bin/env python3
import os
import json
import sqlite3
import urllib.request
from datetime import datetime

class JarvisCoreMatrix:
    def __init__(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.config["DATABASE_PATH"])
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jarvis_business_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                directive_executed TEXT,
                timestamp BIGINT,
                raw_payload TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_telemetry(self, directive, payload):
        conn = sqlite3.connect(self.config["DATABASE_PATH"])
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jarvis_business_logs (directive_executed, timestamp, raw_payload) VALUES (?, ?, ?)",
            (directive, int(datetime.utcnow().timestamp()), json.dumps(payload))
        )
        conn.commit()
        conn.close()
        self.dispatch_alert(f"[Telemetry Locked] {directive}")

    def query_local_llm(self, prompt, model_key="MODEL_NAME"):
        payload = {
            "model": self.config[model_key],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
        url = f"{self.config['OLLAMA_API_BASE']}/api/generate"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode())
                return res["response"]
        except Exception as e:
            return f"Error connecting to local LLM: {str(e)}"

    def execute_system_arm(self, command_string):
        print(f"[*] Core Matrix Executing OS Arm: {command_string}")
        return os.popen(command_string).read()

    def dispatch_alert(self, alert_text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] ALERT: {alert_text}\n"
        with open(self.config["LOG_FILE"], "a") as f:
            f.write(log_message)
        print(log_message.strip())
