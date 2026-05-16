import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from medical_ai_symptom_checker.medical_ai_symptom_checker.app import app

client = TestClient(app)

def test_api_diagnose_smoke():
    resp = client.post("/api/diagnose", json={"symptoms": "fever and cough"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "diagnosis" in data or ("error" in data and data.get("error") == "missing_model")
