#!/usr/bin/env python3
import sys, argparse, json, requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan-range', default='regional-enterprise-targets')
    parser.add_argument('--alert-threshold', default='high')
    args, unknown = parser.parse_known_args()

    prompt = f"Scan range {args.scan_range} for S3 bucket exposures. Threshold: {args.alert_threshold}. Respond ONLY in valid JSON format: {{\"status\": \"secure\", \"findings\": []}}"
    try:
        res = requests.post("http://localhost:11434/v1/chat/completions", json={"model": "jarvis-fast:latest", "messages": [{"role": "user", "content": prompt}]}).json()
        print(res['choices'][0]['message']['content'])
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == '__main__':
    main()
