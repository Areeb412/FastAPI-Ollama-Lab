import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ai_news_summarizer.ai_news_summarizer.app import app

client = TestClient(app)

def test_api_summarize_smoke():
    resp = client.post("/api/summarize", json={"url": "https://example.com/article"})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    assert "summary" in data or ("error" in data and data.get("error") == "missing_model")
