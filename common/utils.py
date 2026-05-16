import os
import subprocess
import logging
import requests
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("common.utils")


def get_ollama_url() -> str:
    return os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")


def is_model_installed(model_name: str) -> bool:
    """Check whether an Ollama model is available locally by calling `ollama list`.

    Returns True if the model name appears in the output; handles missing CLI gracefully.
    """
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=False)
        output = result.stdout + result.stderr
        return model_name in output
    except FileNotFoundError:
        logger.warning("Ollama CLI not found in PATH")
        return False
    except Exception as e:
        logger.exception("Error checking Ollama models: %s", e)
        return False


def call_ollama(prompt: str, model: str, stream: bool = False, timeout: Optional[int] = 30) -> dict:
    """Make a request to the Ollama local generation API and return parsed JSON.

    Raises requests.RequestException on network issues and ValueError on invalid responses.
    """
    url = get_ollama_url()
    payload = {"model": model, "prompt": prompt, "stream": stream}

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            # Fallback: return raw text under 'raw' key
            return {"raw": resp.text}
    except requests.RequestException:
        logger.exception("Ollama request failed")
        raise
