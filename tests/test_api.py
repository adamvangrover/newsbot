from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint():
    # Since we are using mock data when keys are missing, this test should pass without external calls
    response = client.post("/analyze/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert "profile" in data
    assert "news" in data
    assert "stock_data" in data
    assert len(data["news"]) > 0
    assert data["profile"]["ticker"] == "AAPL"
