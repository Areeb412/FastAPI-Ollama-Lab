import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ai_legal_analyzer.ai_legal_analyzer.app import app

client = TestClient(app)

def test_api_analyze_smoke():
    resp = client.post("/api/analyze", json={"text": "This is a sample contract clause."})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "analysis" in data or ("error" in data and data.get("error") == "missing_model")
