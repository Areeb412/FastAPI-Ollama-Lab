
# FastAPI Ollama Lab — Portfolio Collection

Lightweight collection of small AI demo apps showcasing local Ollama model usage with FastAPI backends and minimal modern frontends. Each app is intentionally small, easy to run locally, and designed for a portfolio-style showcase.

Features
- Ten focused demo apps (summarizer, code assistant, content writer, legal analyzer, chatbot, recommender, symptom checker, etc.)
- Clean FastAPI backends with validation, logging, and friendly Ollama model detection
- Modern responsive frontends with distinct color themes and UX improvements
- Shared utilities in `common/` for Ollama interactions

Tech Stack
- Python, FastAPI, Uvicorn
- Ollama (local model server)
- Plain HTML/CSS/JavaScript (no heavy frameworks)

Repository Layout
- Root: repo-level scripts and `requirements.txt`
- `common/`: shared utilities used by all backends
- One folder per demo: `ai_text_summarizer`, `ai_code_assistant`, `ai_content_writer`, `ai_legal_analyzer`, `ai_news_summarizer`, `ai_proofreader`, `ai_virtual_assistant`, `customer_support_chatbot`, `ecommerce_ai_recommender`, `medical_ai_symptom_checker`

Quick Setup (Windows PowerShell)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run an example project (Summarizer):

```powershell
cd ai_text_summarizer\ai_text_summarizer
uvicorn app:app --reload --port 8000
# Open http://localhost:8000
```

Ollama & Models
- The repository does NOT auto-download models.
- If an API response indicates a missing model, install it manually, for example:

```powershell
ollama pull mistral
```

Each project README lists the expected default model name and instructions to pull it.

Testing
- Basic smoke tests are included under each project's `tests/` folder. Run tests with:

```powershell
cd ai_text_summarizer
pytest -q
```

Notes & Troubleshooting
- Ensure `ollama` CLI is installed and available in your PATH when using model-backed features.
- If tests fail due to missing packages, confirm `pip install -r requirements.txt` completed.

Screenshots
- Add screenshots in each project's folder under `static/screenshots/` and reference them in the project README.

Contribution
- Fork, make small focused changes, and open a pull request. Keep UX and design consistent with the theme.

License
- See the `LICENSE` file in the repository root.

# FastAPI-Ollama-Lab
Experimental and production-ready AI applications built with FastAPI, Ollama, and vanilla JavaScript.
