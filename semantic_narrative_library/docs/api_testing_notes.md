# Notes on Testing the Backend API

Besides the simple React frontend, the backend FastAPI can be tested using various methods, including Python scripts with the `requests` library or tools like Postman/Insomnia. These methods provide a direct way to verify API responses and are excellent for backend-focused testing and believability checks.

## Using Python `requests` (Example)

First, ensure the FastAPI server is running (e.g., `uvicorn semantic_narrative_library.api.main:app --reload --port 8000` from the repository root).

Then, you can use a Python script like this:

```python
import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_json(data):
    """Helper to pretty-print JSON data."""
    print(json.dumps(data, indent=2))

def test_api_endpoints():
    print("--- Testing Root ---")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print_json(response.json())
    print("\\n")

    print("--- Testing Get Entity (ind_tech) ---")
    entity_id = "ind_tech"
    response = requests.get(f"{API_BASE_URL}/entities/{entity_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(response.text)
    print("\\n")

    print("--- Testing Get Driver (drv_cloud_adoption) ---")
    driver_id = "drv_cloud_adoption"
    response = requests.get(f"{API_BASE_URL}/drivers/{driver_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(response.text)
    print("\\n")

    print("--- Testing Get Company Details (comp_alpha) ---")
    company_id = "comp_alpha"
    response = requests.get(f"{API_BASE_URL}/companies/{company_id}/details")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(response.text)
    print("\\n")

    print(f"--- Testing Get Direct Drivers for Company ({company_id}) ---")
    response = requests.get(f"{API_BASE_URL}/companies/{company_id}/direct_drivers")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(response.text)
    print("\\n")

    print(f"--- Testing Get Narrative for Company ({company_id}) ---")
    response = requests.get(f"{API_BASE_URL}/companies/{company_id}/narrative")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        # Narrative is plain text
        print(response.text)
    else:
        print(response.text)
    print("\\n")

    print("--- Testing KG Stats ---")
    response = requests.get(f"{API_BASE_URL}/knowledge_graph/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(response.text)
    print("\\n")

    print("--- Testing Non-existent Company (fake_comp) ---")
    company_id_fake = "fake_comp"
    response = requests.get(f"{API_BASE_URL}/companies/{company_id_fake}/details")
    print(f"Status: {response.status_code}") # Expected 404
    print(response.json() if response.headers.get('content-type') == 'application/json' else response.text)
    print("\\n")

if __name__ == "__main__":
    # Ensure 'requests' is installed: pip install requests
    test_api_endpoints()
```

This script can be saved (e.g., `semantic_narrative_library/scripts/test_api_simple.py`) and run from the command line. It provides immediate feedback on the backend's responses.

## Using Jupyter Notebooks

A Jupyter notebook can offer a more interactive way to test:
1.  Install Jupyter: `pip install notebook requests`
2.  Run `jupyter notebook`
3.  Create a new notebook and use similar Python code in cells to call API endpoints and inspect results. This is great for exploratory testing and data validation.

These alternative testing methods complement the React frontend by providing different lenses through which to view and verify the backend's behavior, contributing to the overall "believability" and robustness of the system.
