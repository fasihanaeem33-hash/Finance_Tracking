from playwright.sync_api import sync_playwright
import os
import sys

PORT = int(os.environ.get("PORT", "8501"))
URL = f"http://127.0.0.1:{PORT}/"

KEY_TEXTS = ["Personal Finance Tracker", "Quick Add Transaction", "Add Transaction"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto(URL, timeout=60000)
        # Wait for a few seconds for dynamic content
        for t in KEY_TEXTS:
            try:
                page.wait_for_selector(f"text={t}", timeout=10000)
                print(f"Found '{t}' in page")
                browser.close()
                sys.exit(0)
            except Exception:
                # Not found, try next
                pass
        print("No expected text found in page")
        print(content[:2000])
        browser.close()
        sys.exit(2)
    except Exception as e:
        print("Error loading page:", e)
        browser.close()
        sys.exit(1)
