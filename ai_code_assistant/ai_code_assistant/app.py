from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import logging
import os
import sys
import pathlib

repo_root = str(pathlib.Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from common import utils

logger = logging.getLogger("ai_code_assistant")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Code Assistant")

# Serve static files (HTML, CSS, JS) - use absolute path
static_dir = pathlib.Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

MODEL_NAME = os.getenv("AI_CODE_MODEL", "codellama")


@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))


class CodeRequest(BaseModel):
    prompt: str
    mode: str = "generate"


@app.post("/api/generate")
def api_generate(req: CodeRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    if not utils.is_model_installed(MODEL_NAME):
        return JSONResponse(status_code=400, content={
            "error": "missing_model",
            "message": f"Required Ollama model '{MODEL_NAME}' is not installed. Please run: ollama pull {MODEL_NAME}"
        })

    if req.mode == "generate":
        full_prompt = f"Write a clean, well-documented code snippet: {req.prompt}"
    elif req.mode == "debug":
        full_prompt = f"Debug and fix the following code:\n{req.prompt}"
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    try:
        result = utils.call_ollama(prompt=full_prompt, model=MODEL_NAME)
    except Exception as e:
        logger.exception("Ollama call failed")
        raise HTTPException(status_code=502, detail=str(e))

    code = result.get("response") or result.get("raw") or ""
    return {"code": code}


# Keep compatibility with older frontend route
@app.post("/generate_code")
def generate_code(prompt: str = Form(...), mode: str = Form(...)):
    return api_generate(CodeRequest(prompt=prompt, mode=mode))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=True)
