from playwright.sync_api import sync_playwright
import time
import argparse


def dismiss_consent(page):
    def _try_click(sel, timeout=3000):
        try:
            page.click(sel, timeout=timeout)
            return True
        except Exception:
            return False

    candidates = [
        'text=Accept Cookies', 'text=Accept', 'text=Agree', 'text=Continue', 'text=OK', 'text=Yes',
        "#sp-cc-accept", "input#sp-cc-accept", "button#accept", "button#continue",
        "button[aria-label=\"close\"]",
    ]

    for sel in candidates:
        if _try_click(sel):
            return

    try:
        page.keyboard.press("Escape")
    except Exception:
        pass



def run(pause_seconds: int = 8):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.amazon.in")
        dismiss_consent(page)
        try:
            page.wait_for_selector("input#twotabsearchtextbox", timeout=60000)
        except Exception as e:
            print("Search input not found:", e)
        else:
            page.fill("input#twotabsearchtextbox", "laptop")
            page.press("input#twotabsearchtextbox", "Enter")
            try:
                page.wait_for_selector("div.s-main-slot", timeout=30000)
                print("Search results found")
            except Exception as e:
                print("Search results not found:", e)

        # keep the browser open so you can inspect it
        print(f"Keeping browser open for {pause_seconds} seconds...")
        time.sleep(pause_seconds)
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pause", type=int, default=8, help="Seconds to keep the browser open")
    args = parser.parse_args()
    run(pause_seconds=args.pause)
