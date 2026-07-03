#!/usr/bin/env python3
import sys, argparse, json, requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='audit')
    parser.add_argument('--target-list', default='')
    parser.add_argument('--export-pdf', action='store_true')
    args, unknown = parser.parse_known_args()

    prompt = f"Analyze local SEO competitors for list: {args.target_list}. Mode: {args.mode}. Respond ONLY in valid JSON format: {{\"status\": \"success\", \"competitors\": []}}"
    try:
        res = requests.post("http://localhost:11434/v1/chat/completions", json={"model": "jarvis-fast:latest", "messages": [{"role": "user", "content": prompt}]}).json()
        print(res['choices'][0]['message']['content'])
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == '__main__':
    main()
