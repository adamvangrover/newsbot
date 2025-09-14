import pytest
from fastapi.testclient import TestClient
from newsbot_project_files.backend.app.main import app

client = TestClient(app)

def test_create_portfolio(client):
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio", "description": "a test portfolio"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test portfolio"
    assert data["description"] == "a test portfolio"
    assert "id" in data

def test_read_portfolios(client):
    response = client.get("/api/v1/portfolios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_portfolio(client):
    # First create a portfolio
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio 2", "description": "another test portfolio"})
    assert response.status_code == 200
    data = response.json()
    portfolio_id = data["id"]

    # Now read it
    response = client.get(f"/api/v1/portfolios/{portfolio_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test portfolio 2"
    assert data["id"] == portfolio_id

def test_update_portfolio(client):
    # First create a portfolio
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio 3", "description": "a third test portfolio"})
    assert response.status_code == 200
    data = response.json()
    portfolio_id = data["id"]

    # Now update it
    response = client.put(f"/api/v1/portfolios/{portfolio_id}", json={"name": "updated portfolio", "description": "an updated portfolio"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated portfolio"
    assert data["description"] == "an updated portfolio"

def test_delete_portfolio(client):
    # First create a portfolio
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio 4", "description": "a fourth test portfolio"})
    assert response.status_code == 200
    data = response.json()
    portfolio_id = data["id"]

    # Now delete it
    response = client.delete(f"/api/v1/portfolios/{portfolio_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/v1/portfolios/{portfolio_id}")
    assert response.status_code == 404

def test_add_asset_to_portfolio(client):
    # First create a portfolio
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio 5", "description": "a fifth test portfolio"})
    assert response.status_code == 200
    data = response.json()
    portfolio_id = data["id"]

    # Now add an asset
    asset_to_add = {"asset_id": 123}
    response = client.post(f"/api/v1/portfolios/{portfolio_id}/assets", json=asset_to_add)
    assert response.status_code == 200
    data = response.json()
    assert len(data["assets"]) == 1
    assert data["assets"][0]["asset_id"] == 123

def test_remove_asset_from_portfolio(client):
    # First create a portfolio and add an asset
    response = client.post("/api/v1/portfolios/", json={"name": "test portfolio 6", "description": "a sixth test portfolio"})
    assert response.status_code == 200
    data = response.json()
    portfolio_id = data["id"]
    asset_to_add = {"asset_id": 456}
    response = client.post(f"/api/v1/portfolios/{portfolio_id}/assets", json=asset_to_add)
    assert response.status_code == 200
    data = response.json()
    assert len(data["assets"]) == 1
    assert data["assets"][0]["asset_id"] == 456

    # Now remove the asset
    response = client.delete(f"/api/v1/portfolios/{portfolio_id}/assets/456")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/v1/portfolios/{portfolio_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["assets"]) == 0
