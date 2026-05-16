import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from customer_support_chatbot.customer_support_chatbot.app import app

client = TestClient(app)

def test_api_chat_smoke():
    resp = client.post("/api/chat", json={"message": "How do I reset my password?"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "reply" in data or ("error" in data and data.get("error") == "missing_model")
