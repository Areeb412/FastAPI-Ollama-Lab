from fastapi.testclient import TestClient
from ai_virtual_assistant.app import app

client = TestClient(app)

def test_api_ask_smoke():
    resp = client.post("/api/ask", json={"question": "What is the weather like?"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "answer" in data or ("error" in data and data.get("error") == "missing_model")
