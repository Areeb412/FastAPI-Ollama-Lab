from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os
import json
import pathlib

app = FastAPI()

# Serve static files (HTML, CSS, JS) - use absolute path
static_dir = pathlib.Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi"  # Using Phi-2 for legal document analysis


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))


@app.post("/api/analyze")
def analyze_legal_json(req: AnalyzeRequest):
    """Analyze legal text via JSON API"""
    prompt = f"Extract key insights from the following legal document:\n{req.text}\nSummarize important clauses, risks, and obligations."

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=30
        )
        
        response_data = response.json()
        analysis = response_data.get("response", "No analysis generated.")
        return {"analysis": analysis}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")


@app.post("/analyze_legal_text")
def analyze_legal_text(text: str = Form(...)):
    """Legacy form-based endpoint"""
    headers = {"Content-Type": "application/json"}

    prompt = f"Extract key insights from the following legal document:\n{text}\nSummarize important clauses, risks, and obligations."

    try:
        # Send the input text to Ollama for legal analysis
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            headers=headers
        )

        # Log the response for debugging
        print("Ollama Response:", response.text)

        # Ensure valid JSON response
        response_data = response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Ollama: {response_data}")

        # Extract legal insights
        legal_insights = json_response.get("response", "No insights generated.")
        return {"insights": legal_insights}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)








