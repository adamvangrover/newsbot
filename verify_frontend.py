from playwright.sync_api import Page, expect, sync_playwright
import os

def test_frontend_navigation(page: Page):
    print("Navigating to home...")
    page.goto("http://localhost:4173/")
    # Title might be generic "Vite + React + TS" if index.html wasn't updated, so checking heading or text is safer if title fails.
    # But usually <title> is in index.html. Let's assume it's default or we updated it.
    # I didn't update index.html title explicitly in my plan, but it might be there.
    # I'll check for "NewsBot Nexus" text on home page if title fails.

    print("Navigating to Projections...")
    page.goto("http://localhost:4173/#/projections")
    # Wait for heading
    expect(page.get_by_role("heading", name="Evolutionary Projections")).to_be_visible()
    page.screenshot(path="/home/jules/verification/projections.png")

    print("Navigating to Agents...")
    page.goto("http://localhost:4173/#/agents")
    expect(page.get_by_role("heading", name="Agent Orchestrator")).to_be_visible()
    page.screenshot(path="/home/jules/verification/agents.png")

    print("Navigating to Status...")
    page.goto("http://localhost:4173/#/status")
    expect(page.get_by_role("heading", name="System Status")).to_be_visible()
    page.screenshot(path="/home/jules/verification/status.png")

if __name__ == "__main__":
    os.makedirs("/home/jules/verification", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_frontend_navigation(page)
        finally:
            browser.close()
