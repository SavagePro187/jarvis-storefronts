#!/usr/bin/env python3
import sys
import json
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def classify_intent_stream(raw_text_input):
    classification_prompt = (
        "Classify the following inbound business intent into exactly ONE category token choice.\n"
        f"Input: \"{raw_text_input}\"\n\n"
        "Tokens:\n"
        "- B2B_LEAD_GEN (Standard outreach requirements)\n"
        "- REMOVE_REQUEST (Opt-out requests)\n"
        "- PARTNER_INQUIRY (Joint venture talk)\n\n"
        "STRICT RULE: Output only the exact token name string. Do not include punctuation or sentences."
    )
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": classification_prompt,
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 15}
    }
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=60.0)
        token = res.json().get("response", "").strip()
        print(f"[SUCCESS] Intent Classified ➔ [{token}]")
        return token
    except Exception as e:
        print(f"[❌] Classification failure: {e}")
        return "B2B_LEAD_GEN"

if __name__ == "__main__":
    sample_query = sys.argv[1] if len(sys.argv) > 1 else "Please take me off your distribution parameters."
    classify_intent_stream(sample_query)
