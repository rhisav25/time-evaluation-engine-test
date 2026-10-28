# API Test — simple one-at-a-time runner

## How to use

1. Open `test_api.py`
2. Change the `INPUT_FILE` line at the top:
   ```python
   INPUT_FILE = "scenarios/01_example_a.json"
   ```
3. Run it:
   ```bash
   python3 test_api.py
   ```
4. The response is saved to `output.json` and also printed to the terminal.

To test a different scenario — change `INPUT_FILE` and run again. One at a time, no loop.

> Note: `output.json` (and any `output_*.json`) are generated on each run and are
> git-ignored — they are not committed.

## Trace id (for debugging & validation)

Every API response carries an `X-Trace-Id` header. The runner surfaces it in two
places so a run can be cross-checked against the server logs:

1. **In the terminal** — on the status line after the request completes:
   ```
   ← status: 200 · trace: 2085dd3f-96a3-4732-badc-9d43300c66ba
     response saved to: output.json
   ```
2. **In the saved file** — folded in as the first field of the JSON body:
   ```json
   {
     "traceId": "2085dd3f-96a3-4732-badc-9d43300c66ba",
     "dailyResults": [ ... ],
     "weeklyResults": [ ... ]
   }
   ```

If the response isn't JSON (e.g. an error page), the trace id is prepended as an
`X-Trace-Id:` line instead. When the header is absent it shows as `—`. Grep the
server logs for the trace id to line up a response with exactly what the engine did.

## Scenarios included

| File | What it tests | Expected result |
|---|---|---|
| `01_example_a.json` | Heavy days (42h week) | 4h daily OT, 0h weekly OT (reconciled to 0) |
| `02_example_b.json` | Spread week (46h) | 2h daily OT, 4h weekly OT reconciled |
| `03_sunday_work.json` | Plain Sunday work | sunday-work = 300 min on Sunday |
| `04_holiday_wins.json` | Sunday also a holiday | public-holiday-work gets 300, sunday-work = 0 |
| `05_outside_window.json` | Mon 07:00–19:00 vs 08:00–18:00 | outside-window = 120 min on Mon |
| `06_overlap_should_fail.json` | Overlapping intervals | HTTP 400 error |

## Requirements

- Python 3 (stdlib only — no pip install needed)
- API running at `http://localhost:8080` (change `API_URL` in `test_api.py` if different)
