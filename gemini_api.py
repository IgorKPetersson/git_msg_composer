#!/usr/bin/env python3
"""
Gemini API helper script for git commit message generation
"""
import sys
import json
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python gemini_api.py <prompt_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    prompt_file = sys.argv[1]
    output_file = sys.argv[2]
    api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    # Read prompt
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except Exception as e:
        print(f"Error reading prompt file: {e}", file=sys.stderr)
        sys.exit(1)

    # Prepare API request
    payload = {
        'contents': [{
            'parts': [{'text': prompt}]
        }]
    }

    # Call Gemini API
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']

        # Write response
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        # Also print to stdout for immediate feedback
        print(text)

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response: {e}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
