from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Dashboard Home
        print("Navigating to Home...")
        page.goto("http://localhost:4173/")
        page.wait_for_selector('text=System Dashboard', timeout=10000)
        page.screenshot(path="verification/dashboard_home.png")
        print("Captured dashboard_home.png")

        # 2. Performance Dashboard
        print("Navigating to Performance Dashboard...")
        # Click the menu item
        page.click('text=Performance')
        page.wait_for_selector('text=Analyst Playbook: AAPL', timeout=10000)
        # Wait for charts to render (they have animation)
        time.sleep(2)
        page.screenshot(path="verification/performance_dashboard.png")
        print("Captured performance_dashboard.png")

        # 3. Federated Learning
        print("Navigating to Federated Learning...")
        page.click('text=Federated Learning')
        page.wait_for_selector('text=Federated Learning Simulation', timeout=10000)
        time.sleep(2)
        page.screenshot(path="verification/federated_learning.png")
        print("Captured federated_learning.png")

        # 4. Knowledge Graph
        print("Navigating to Knowledge Graph...")
        page.click('text=Knowledge Graph')
        page.wait_for_selector('text=Semantic Knowledge Graph', timeout=10000)
        time.sleep(2)
        page.screenshot(path="verification/knowledge_graph.png")
        print("Captured knowledge_graph.png")

        browser.close()

if __name__ == "__main__":
    run()
