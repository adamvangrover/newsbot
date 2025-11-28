from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_impact_endpoint():
    payload = {
        "article_id": 123,
        "headline": "Fed announces Rate Hike",
        "publish_timestamp_utc": "2023-10-01T12:00:00Z",
        "tickers_mentioned": ["AAPL"],
        "ingestion_timestamp": "2023-10-01T12:00:00Z"
    }

    response = client.post("/api/reasoning/impact", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["original_event"] == "Fed announces Rate Hike"
    assert data["signal_strength"] == "High Signal"
    assert len(data["impact_chains"]) > 0
    assert data["impact_chains"][0]["impact_type"] == "PriceDrop"

def test_simulate_scenario_endpoint():
    payload = {
        "name": "Test Scenario",
        "events": [
            {
                "headline": "CEO Resigns from Acme Corp",
                "tickers_mentioned": ["ACME"]
            },
            {
                "headline": "Acme Corp reports record revenue",
                "tickers_mentioned": ["ACME"]
            }
        ]
    }

    response = client.post("/api/reasoning/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_name"] == "Test Scenario"
    assert len(data["outcomes"]) == 2
    assert data["outcomes"][0]["impact_chains"][0]["impact_type"] == "PriceDrop" # CEO Resign -> Negative
    assert data["outcomes"][1]["impact_chains"][0]["impact_type"] == "PriceSurge" # Record Revenue -> Positive
