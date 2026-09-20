#!/usr/bin/env python3
"""
Custom Wazuh-to-Shuffle SOAR Integration Bridge
Reads JSON alert files delivered by wazuh-integratord and posts them to Shuffle.
"""

import sys
import json
import requests

def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    alert_file_path = sys.argv[1]
    hook_url = sys.argv[3]

    try:
        with open(alert_file_path, "r", encoding="utf-8") as alert_file:
            alert_json = json.load(alert_file)

        headers = {"Content-Type": "application/json"}
        response = requests.post(hook_url, json=alert_json, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        sys.stderr.write(f"Error forwarding alert to Shuffle: {exc}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
