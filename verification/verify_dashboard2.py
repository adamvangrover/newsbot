from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to home
        page.goto("http://localhost:8000")
        page.wait_for_selector("text=NewsBot Nexus")
        page.screenshot(path="verification/dashboard_home.png")
        print("Home screenshot taken.")

        # Click on Scenario Simulator
        page.click("text=Scenario Simulator")
        page.wait_for_selector("text=Configure Simulation")

        # Fill in scenario details
        page.fill("input[value='Custom Scenario']", "Frontend Test Scenario")
        page.click("text=Run Simulation")

        # Wait for results (mock is fast)
        page.wait_for_selector("text=Simulation Results")

        # Take screenshot of results
        page.screenshot(path="verification/dashboard_simulator.png")
        print("Simulator screenshot taken.")

        browser.close()

if __name__ == "__main__":
    verify_dashboard()
