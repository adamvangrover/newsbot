from playwright.sync_api import Page, expect, sync_playwright

def verify_frontend(page: Page):
    # 1. Landing Page
    print("Navigating to Home...")
    page.goto("http://localhost:5173/")

    # Wait for content to load
    expect(page.get_by_text("Synthetic Reality Engine")).to_be_visible()

    # Screenshot Home
    print("Screenshotting Home...")
    page.screenshot(path="/home/jules/verification/01_home.png")

    # 2. Dashboard
    print("Navigating to Dashboard...")
    page.click("text=Launch Dashboard")

    expect(page.get_by_text("OPERATIONAL DASHBOARD")).to_be_visible()

    # Check Sidebar
    expect(page.get_by_role("link", name="Synthetic Data")).to_be_visible()

    print("Screenshotting Dashboard...")
    page.screenshot(path="/home/jules/verification/02_dashboard.png")

    # 3. Showcase
    print("Navigating to Showcase...")
    page.click("text=Synthetic Data")

    expect(page.get_by_text("Synthetic Data Showcase")).to_be_visible()
    expect(page.get_by_text("Synthetic Corporate News")).to_be_visible()

    print("Screenshotting Showcase...")
    page.screenshot(path="/home/jules/verification/03_showcase.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_frontend(page)
            print("Verification complete!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()
