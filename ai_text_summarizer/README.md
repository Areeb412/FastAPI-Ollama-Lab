# Summar.ai — AI Text Summarizer

What it does
- Small demo that summarizes long text using a local Ollama model.

Features
- Responsive single-page frontend
- FastAPI backend with model detection and helpful error messages

How it works
- Frontend calls `POST /api/summarize` with JSON `{ text }`.
- Backend checks that the configured Ollama model is installed and then forwards the prompt to the local Ollama API.

Setup
1. Install Python dependencies: `pip install -r requirements.txt` (from repo root).
2. Run the app:

```powershell
cd ai_text_summarizer\ai_text_summarizer
uvicorn app:app --reload --port 8000
```

Ollama
- This project expects a model named `mistral` by default. To install:

```powershell
ollama pull mistral
```

API
- `POST /api/summarize` — JSON `{ "text": "..." }` returns `{ "summary": "..." }` or `{ "error": "missing_model", "message": "..." }` when model is missing.

UI Preview
- Open `http://localhost:8000` after starting the app.

Troubleshooting
- If you see `missing_model`, run the `ollama pull` command above.
- Ensure `ollama` CLI is in your PATH.
