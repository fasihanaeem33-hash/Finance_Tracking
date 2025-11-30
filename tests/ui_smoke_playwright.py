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
        # Wait for dynamic content and confirm main strings render
        for t in KEY_TEXTS:
            try:
                page.wait_for_selector(f"text={t}", timeout=10000)
                print(f"Found '{t}' in page")
            except Exception:
                print(f"Did not find '{t}' in page (may be hidden)")

        # Try to perform a form submit in the main form
        # Generate a unique category to assert it shows up
        import time
        unique_cat = f"UITest_{int(time.time())}"
        # Fill amount, category, and note (main form has inputs with labels)
        try:
            page.get_by_label('Amount').fill('123.45')
        except Exception:
            # If label-based selector fails, try input placeholder fallback
            inputs = page.locator('input')
            if inputs.count() > 0:
                inputs.nth(0).fill('123.45')
        try:
            page.get_by_label('Category').fill(unique_cat)
        except Exception:
            # fallback: use the second text input
            text_inputs = page.locator('input[type="text"]')
            if text_inputs.count() >= 1:
                text_inputs.nth(0).fill(unique_cat)
        try:
            page.get_by_label('Note (optional)').fill('Playwright e2e')
        except Exception:
            pass

        # Click the Add Transaction button that is inside the main (left) column
        buttons = page.get_by_role('button', name='Add Transaction')
        count = buttons.count()
        if count == 0:
            print('No Add Transaction buttons found')
            browser.close()
            sys.exit(2)
        clicked = False
        for i in range(count):
            try:
                btn = buttons.nth(i)
                if not btn.is_visible():
                    continue
                box = btn.bounding_box()
                if not box:
                    continue
                # Heuristic: left column should have a smaller x coordinate (left side)
                if box['x'] < 600:
                    btn.click()
                    clicked = True
                    break
            except Exception:
                continue
        if not clicked:
            # fallback: click the last one
            buttons.nth(count - 1).click()

        # Wait for the new category text to appear in the page after submit
        try:
            page.wait_for_selector(f"text={unique_cat}", timeout=10000)
            print('Success: new transaction is visible on the page')
            browser.close()
            sys.exit(0)
        except Exception as e:
            print('Failed to find the new transaction after submit:', e)
            # as fallback, open Raw stored JSON expander and search
            try:
                page.get_by_text('Raw stored JSON').click()
                page.wait_for_timeout(500)
                content = page.content()
                if unique_cat in content:
                    print('Found in raw JSON')
                    browser.close()
                    sys.exit(0)
            except Exception:
                pass
            browser.close()
            sys.exit(3)
        print("No expected text found in page")
        print(content[:2000])
        browser.close()
        sys.exit(2)
    except Exception as e:
        print("Error loading page:", e)
        browser.close()
        sys.exit(1)
