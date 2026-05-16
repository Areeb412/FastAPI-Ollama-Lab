# AI Code Assistant

What it does
- A simple code assistant demo powered by local Ollama models.

Features
- FastAPI backend and minimal frontend for interacting with models.

Setup & Usage
1. Install dependencies: `pip install -r requirements.txt`.
2. Start the service from the project folder:

```powershell
cd ai_code_assistant\ai_code_assistant
uvicorn app:app --reload --port 8001
```

Ollama
- Install required model if prompted: `ollama pull <model-name>`

API
- Check `app.py` for endpoints and behavior.

Troubleshooting
- Ensure Ollama is installed and available in PATH.
