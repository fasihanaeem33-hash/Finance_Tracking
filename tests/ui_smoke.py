import os
import time
import urllib.request
import sys

PORT = int(os.environ.get("PORT", "8501"))
URL = f"http://127.0.0.1:{PORT}/"

KEY_STRINGS = ["Personal Finance Tracker", "Quick Add Transaction", "Add Transaction"]

# Wait for server to become responsive
for i in range(60):
    try:
        with urllib.request.urlopen(URL, timeout=5) as r:
            html = r.read().decode("utf-8", errors="ignore")
            # Check if any of our expected strings is present
            for s in KEY_STRINGS:
                if s in html:
                    print(f"Found expected string: {s}")
                    sys.exit(0)
            print("Server responded but no expected UI text found - failing")
            # For debugging, print a small snippet
            print(html[:1000])
            sys.exit(2)
    except Exception as e:
        print(f"Waiting for server... ({i}) - {e}")
        time.sleep(1)

print("Timed out waiting for server to respond", file=sys.stderr)
sys.exit(1)
