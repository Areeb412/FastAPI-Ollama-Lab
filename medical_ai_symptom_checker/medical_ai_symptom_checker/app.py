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

logger = logging.getLogger("medical_ai_symptom_checker")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Medical AI Symptom Checker")

# Serve static files (HTML, CSS, JS) - use absolute path
static_dir = pathlib.Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

MODEL_NAME = os.getenv("AI_MEDICAL_MODEL", "medllama2")


@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))


class SymptomRequest(BaseModel):
    symptoms: str


@app.post("/api/diagnose")
def api_diagnose(req: SymptomRequest):
    if not req.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms are required")

    if not utils.is_model_installed(MODEL_NAME):
        return JSONResponse(status_code=400, content={
            "error": "missing_model",
            "message": f"Required Ollama model '{MODEL_NAME}' is not installed. Please run: ollama pull {MODEL_NAME}"
        })

    prompt = (
        f"You are a medical AI assistant. Provide possible explanations and general next steps for the following symptoms."
        f"\n\nSymptoms: {req.symptoms}\n\nNote: do not provide a diagnosis; advise to consult a medical professional."
    )

    try:
        result = utils.call_ollama(prompt=prompt, model=MODEL_NAME)
    except Exception as e:
        logger.exception("Ollama call failed")
        raise HTTPException(status_code=502, detail=str(e))

    diagnosis = result.get("response") or result.get("raw") or ""
    return {"diagnosis": diagnosis}


@app.post("/analyze_symptoms")
def analyze_symptoms(symptoms: str = Form(...)):
    return api_diagnose(SymptomRequest(symptoms=symptoms))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8009)), reload=True)









