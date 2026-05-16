import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ai_content_writer.ai_content_writer.app import app

client = TestClient(app)

def test_api_generate_smoke():
    resp = client.post("/api/generate", json={"topic": "AI", "style": "professional"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "content" in data or ("error" in data and data.get("error") == "missing_model")
