#!/usr/bin/env python3
import os
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "local-bypass"
import urllib.request
import json

N8N_URL = "http://localhost:5678/api/v1/workflows"

workflow_payload = {
    "name": "Jarvis Sovereign Production Ingestion Matrix",
    "active": True,
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "jarvis-gateway",
                "responseMode": "responseNode",
                "options": {}
            },
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2.1,
            "position":,
            "id": "webhook-trigger",
            "name": "Webhook"
        },
        {
            "parameters": {
                "operation": "executeQuery",
                "query": "CREATE TABLE IF NOT EXISTS jarvis_business_logs (\n    id SERIAL PRIMARY KEY,\n    directive_executed TEXT,\n    timestamp BIGINT,\n    raw_payload TEXT\n);\n\nINSERT INTO jarvis_business_logs (directive_executed, timestamp, raw_payload) \nVALUES (\n    '{{ $json.body.global_directive }}',\n    {{ $json.body.timestamp }},\n    '{{ JSON.stringify($json.body) }}'\n);"
            },
            "type": "n8n-nodes-base.postgres",
            "typeVersion": 2.6,
            "position":,
            "id": "postgres-logger",
            "name": "PostgreSQL Logger"
        },
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": "{\n  \"workflow_status\": \"executed_successfully\",\n  \"database_logging\": \"committed\"\n}",
                "options": {
                    "responseCode": 200
                }
            },
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.5,
            "position":,
            "id": "respond-webhook",
            "name": "Respond to Webhook"
        }
    ],
    "connections": {
        "Webhook": {
            "main": [
                [
                    {
                        "node": "PostgreSQL Logger",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "PostgreSQL Logger": {
            "main": [
                [
                    {
                        "node": "Respond to Webhook",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "settings": {}
}

req = urllib.request.Request(
    N8N_URL, 
    data=json.dumps(workflow_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"[+] Success: Production canvas deployed and activated. (Status: {response.getcode()})")
except Exception as e:
    print(f"[-] Automated deployment failed. Error: {e}")
