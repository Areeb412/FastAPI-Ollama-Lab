import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ecommerce_ai_recommender.ecommerce_ai_recommender.app import app

client = TestClient(app)

def test_api_recommend_smoke():
    resp = client.post("/api/recommend", json={"user_input": "gaming laptop, budget $1200"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "recommendations" in data or ("error" in data and data.get("error") == "missing_model")
