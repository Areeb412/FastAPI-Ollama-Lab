# AI Content Writer

What it does
- Generate blog posts, outlines, and short-form content via a local model.

Setup & Usage
1. Install dependencies: `pip install -r requirements.txt`.
2. Start the app:

```powershell
cd ai_content_writer\ai_content_writer
uvicorn app:app --reload --port 8002
```

Ollama
- Pull the model manually if requested: `ollama pull <model-name>`
