#!/usr/bin/env python3
"""
Example usage of ppxl_lite - Lightweight Perplexity AI client

This example shows how to use both anonymous and pro modes.
"""

import json
from client import Client

def main():
    print("="*60)
    print("PPXL Lite Example")
    print("="*60)

    # Anonymous search example
    print("\n1. Anonymous Search (no cookies needed):")
    print("   client = Client()")
    print("   response = client.search('What is AI?', mode='auto')")

    # Pro mode example with cookies
    print("\n2. Pro Search (requires cookies):")
    print("   # First save your cookies to cookies.json")
    print("   with open('cookies.json', 'r') as f:")
    print("       cookies = json.load(f)")
    print("   ")
    print("   client = Client(cookies)")
    print("   response = client.search('Complex query', mode='pro', model='claude-4.5-sonnet')")

    # Available models
    print("\n3. Available Models:")
    print("   - Auto mode: default (anonymous)")
    print("   - Pro mode: sonar, gpt-5.2, claude-4.5-sonnet, grok-4.1")
    print("   - Reasoning mode: claude-4.5-sonnet-thinking, kimi-k2-thinking, grok-4.1-reasoning")
    print("   - Deep research: default")

    # How to get cookies
    print("\n4. How to Get Cookies:")
    print("   1. Login to perplexity.ai")
    print("   2. Open DevTools (F12)")
    print("   3. Network tab → Refresh")
    print("   4. Copy as cURL → curlconverter.com")
    print("   5. Extract cookies → save to cookies.json")

    print("\nReady to use!")
    print("   Uncomment the code below to test with your cookies:")
    print("""
# Uncomment to test:
try:
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    client = Client(cookies)
    response = client.search('Test', mode='pro')
    print('Working!' if response else 'Check cookies')
except FileNotFoundError:
    print('Create cookies.json first')
""")

if __name__ == "__main__":
    main()