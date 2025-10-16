from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from fastapi import BackgroundTasks
from etl.ingest_argovis import ingest_data

client = TestClient(app)

@patch.object(BackgroundTasks, "add_task")
def test_ingest_endpoint(mock_add_task):
    response = client.post("/api/ingest")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingestion started in the background."}
    mock_add_task.assert_called_once_with(ingest_data)
