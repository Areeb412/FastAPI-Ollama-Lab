import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from ai_text_summarizer.ai_text_summarizer.app import app

client = TestClient(app)


def test_summarize_endpoint_returns_json():
    """Check that endpoint returns JSON with either `summary` or `error` key."""
    resp = client.post("/api/summarize", json={"text": "This is a test text to summarize."})
    assert resp.headers["content-type"].startswith("application/json")
    data = resp.json()
    assert isinstance(data, dict)
    # Either the model is missing (friendly error) or we get a summary
    assert "summary" in data or ("error" in data and data.get("error") == "missing_model")
