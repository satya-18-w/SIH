from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch("app.routers.ingest.ingest_data")
def test_ingest_endpoint(mock_ingest_data):
    response = client.post("/api/ingest")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingestion started in the background."}
    mock_ingest_data.assert_called_once()
