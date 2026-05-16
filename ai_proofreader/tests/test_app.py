import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ai_proofreader.ai_proofreader.app import app

client = TestClient(app)

def test_api_proofread_smoke():
    resp = client.post("/api/proofread", json={"text": "This are bad grammar."})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "proofread" in data or ("error" in data and data.get("error") == "missing_model")
