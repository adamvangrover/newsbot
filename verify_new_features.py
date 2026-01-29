from playwright.sync_api import Page, expect, sync_playwright
import os

def test_new_features(page: Page):
    print("Navigating to Federated Learning...")
    page.goto("http://localhost:4173/#/federated")
    # Wait for heading
    expect(page.get_by_role("heading", name="Federated Learning")).to_be_visible()
    # Check for stats (Accuracy or Round might be "Checking..." or updated)
    # Just snapshot the UI structure
    page.screenshot(path="/home/jules/verification/federated.png")

    print("Navigating to Plugins...")
    page.goto("http://localhost:4173/#/plugins")
    expect(page.get_by_role("heading", name="Plugin Manager")).to_be_visible()
    # Check if the mock plugins (or loaded ones) are visible
    # Ideally "market_volatility_monitor" if backend was connected, but this is static preview mostly unless we proxy
    # The frontend code falls back to mocks if fetch fails, so we should see cards.
    page.screenshot(path="/home/jules/verification/plugins.png")

if __name__ == "__main__":
    os.makedirs("/home/jules/verification", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_new_features(page)
        finally:
            browser.close()
