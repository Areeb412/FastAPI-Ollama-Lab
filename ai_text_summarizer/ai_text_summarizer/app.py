from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import logging
import os
import sys
import pathlib

# Ensure the repository root is on sys.path so `common` can be imported when running
# from the project folder. Adjust parents index if the layout changes.
repo_root = str(pathlib.Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from common import utils

logger = logging.getLogger("ai_text_summarizer")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Text Summarizer")

# Serve static files (HTML, CSS, JS) - use absolute path
static_dir = pathlib.Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

MODEL_NAME = os.getenv("AI_SUMMARIZER_MODEL", "mistral")


@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))


class SummarizeRequest(BaseModel):
    text: str


@app.post("/api/summarize")
def summarize(req: SummarizeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    # Check whether the model is installed locally
    if not utils.is_model_installed(MODEL_NAME):
        msg = {
            "error": "missing_model",
            "message": f"Required Ollama model '{MODEL_NAME}' is not installed. Please run: ollama pull {MODEL_NAME}"
        }
        return JSONResponse(status_code=400, content=msg)

    prompt = f"Summarize the following text:\n\n{req.text}\n\nBriefly summarize in 3-5 sentences."

    try:
        result = utils.call_ollama(prompt=prompt, model=MODEL_NAME)
    except Exception as e:
        logger.exception("Ollama call failed")
        raise HTTPException(status_code=502, detail=str(e))

    # Ollama may return different shapes; try common keys
    summary = result.get("response") or result.get("result") or result.get("raw") or ""
    return {"summary": summary}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)









