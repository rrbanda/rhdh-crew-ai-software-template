from fastapi import FastAPI, HTTPException
from src.tasks import get_leopard_task
from crewai import Crew
import json
import requests
import logging
import yaml
import os
from dotenv import load_dotenv

# ✅ Load .env for local development
load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Load configuration from environment variables or YAML file
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE", "/app/configs/config.yaml")

config = {}
if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except Exception as e:
        logger.error(f"❌ Error loading config file: {e}")

# ✅ Function to load values from ENV with fallback to config.yaml
def get_config_value(key_path: str, env_var: str, default=None):
    """Retrieve config value from ENV or YAML with default fallback."""
    env_value = os.getenv(env_var)
    if env_value:
        return env_value

    keys = key_path.split(".")
    temp_config = config
    for key in keys:
        if isinstance(temp_config, dict):
            temp_config = temp_config.get(key, None)
        else:
            return default

    return temp_config if temp_config is not None else default

# ✅ Load LLM API configurations
LLM_API_KEY = get_config_value("llm.api_key", "LLM_API_KEY", None)  # Optional API key
LLM_MODEL_NAME = get_config_value("llm.model_name", "LLM_MODEL", "deepseek-r1-distill-qwen-14b")
LLM_BASE_URL = get_config_value("llm.base_url", "LLM_BASE_URL")
FORMATTER_URL = get_config_value("formatter.api_url", "FORMATTER_API_URL", "http://localhost:8001/process")

# ✅ Debug Logs
logger.info(f"🔍 Loaded LLM_MODEL: {LLM_MODEL_NAME}")
logger.info(f"🔍 Loaded LLM_BASE_URL: {LLM_BASE_URL}")
logger.info(f"🔍 LLM_API_KEY: {'SET' if LLM_API_KEY else 'NOT SET'}")

@app.get("/")
def home():
    """Basic home endpoint."""
    return {"message": "Leopard Pont des Arts API is running!"}

@app.get("/health")
def health():
    """Health check endpoint to verify API readiness."""
    return {"status": "ok"}

@app.get("/leopard-crossing")
def leopard_crossing():
    """Returns raw agent response."""
    return execute_leopard_task()

@app.get("/leopard-crossing-ui")
def leopard_crossing_ui():
    """Returns formatted agent response via Formatter API."""
    raw_result = execute_leopard_task()
    return call_formatter(raw_result)

def call_formatter(data):
    """Send response to the external formatter service if available."""
    payload = {"format": "json", "data": data}
    try:
        response = requests.post(FORMATTER_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Formatter service request error: {e}")
        return data  # Fallback to raw response

def execute_leopard_task():
    """Runs the CrewAI agent and returns computed response."""
    if not LLM_BASE_URL:
        return {"error": "Missing LLM API URL in config"}

    task = get_leopard_task()
    crew = Crew(agents=[task.agent], tasks=[task], verbose=True)

    try:
        result = crew.kickoff()
        return json.loads(result.raw) if hasattr(result, "raw") else {"error": "Unexpected response"}
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON response from CrewAI")
        return {"error": "Invalid JSON response"}
    except Exception as e:
        logger.error(f"❌ CrewAI Execution Error: {e}")
        return {"error": "Internal error while executing task"}

# ✅ Ensure `app` is available when running `uvicorn src.api:app`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
