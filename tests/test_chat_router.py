from fastapi.testclient import TestClient
from app.main import app
from app.services.rag import RagService
from app.routers.chat import get_rag_service
from unittest.mock import MagicMock

client = TestClient(app)

def test_chat_endpoint():
    # Mock the RagService
    mock_rag_service = MagicMock(spec=RagService)
    mock_rag_service.process_query.return_value = {
        "query": "hello",
        "retrieved_context": [],
        "llm_response": "Hello! How can I help you today?",
        "provenance": []
    }
    
    # Dependency override
    app.dependency_overrides[get_rag_service] = lambda: mock_rag_service

    response = client.post(
        "/api/chat",
        json={"session_id": "test", "message": "hello"}
    )
    
    assert response.status_code == 200
    assert response.json()["llm_response"] == "Hello! How can I help you today?"
    
    # Clear the dependency override
    app.dependency_overrides = {}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

