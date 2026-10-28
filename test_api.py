#!/usr/bin/env python3

import json
import urllib.request
import urllib.error

INPUT_FILE  = "scenarios/01_example_a.json"
OUTPUT_FILE = "output.json"
API_URL     = "http://localhost:8080/api/evaluations"


def main():
    # 1. Load the input JSON
    with open(INPUT_FILE) as f:
        payload = json.load(f)

    print(f"→ POST {API_URL}")
    print(f"  input: {INPUT_FILE}")

    # 2. POST to the API
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            trace_id = resp.headers.get("X-Trace-Id", "—")
    except urllib.error.HTTPError as e:
        # 4xx / 5xx response — still save the body
        status = e.code
        body = e.read().decode("utf-8")
        trace_id = e.headers.get("X-Trace-Id", "—") if e.headers else "—"
    except urllib.error.URLError as e:
        print(f"✗ connection error: {e}")
        print(f"  Is the API running at {API_URL}?")
        return

    # 3. Pretty-print the response (with the trace id) and save it
    try:
        parsed = json.loads(body)
        # Fold the trace id into the saved output so it's available for debugging
        if isinstance(parsed, dict):
            parsed = {"traceId": trace_id, **parsed}
        pretty = json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        pretty = f"X-Trace-Id: {trace_id}\n{body}"

    with open(OUTPUT_FILE, "w") as f:
        f.write(pretty)

    # 4. Show what happened
    print(f"← status: {status} · trace: {trace_id}")
    print(f"  response saved to: {OUTPUT_FILE}")
    print()
    print(pretty)


if __name__ == "__main__":
    main()
