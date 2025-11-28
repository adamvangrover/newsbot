from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_perform_analysis():
    response = client.post("/analyze/", json={"data": "test"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Analysis pipeline initiated."}
