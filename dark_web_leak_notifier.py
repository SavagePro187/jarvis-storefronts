#!/usr/bin/env python3
import sys, argparse, json, requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--monitor-domains', default='')
    parser.add_argument('--api-sync', default='n8n')
    args, unknown = parser.parse_known_args()

    prompt = f"Check dark web leaks for domains in: {args.monitor_domains}. Sync via {args.api_sync}. Respond ONLY in valid JSON format: {{\"status\": \"secure\", \"alerts\": []}}"
    try:
        res = requests.post("http://localhost:11434/v1/chat/completions", json={"model": "jarvis-fast:latest", "messages": [{"role": "user", "content": prompt}]}).json()
        print(res['choices'][0]['message']['content'])
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == '__main__':
    main()
