import requests
import json
import yaml
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)

# ✅ Load LLM Provider Config from ConfigMap
CONFIG_FILE_PATH = "configs/llm_provider_config.yaml"
config = {}

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError as e:
        logger.error(f"❌ Config file not found: {e}")

# ✅ Extract JSON from response function (Fixes markdown-wrapped JSON)
def extract_json(response_text):
    """Extract JSON part from LLM response, handling markdown formatting."""
    response_text = response_text.strip("`")  # Remove markdown if wrapped
    try:
        json_obj = json.loads(response_text)
        return json.dumps(json_obj, indent=2)
    except json.JSONDecodeError:
        logger.error("❌ LLM response is not valid JSON")
        return json.dumps({"error": "Invalid JSON received from LLM"})


class CustomLLM:
    def __init__(self):
        """Load LLM Configuration Dynamically from OpenShift ConfigMap"""
        self.provider = os.getenv("ACTIVE_PROVIDER", "default")  # Read from OpenShift ConfigMap
        llm_config = config.get("llms", {}).get(self.provider, {})

        # ✅ Dynamically get values from ConfigMap or fallback to .env
        self.base_url = os.getenv(f"{self.provider.upper()}_BASE_URL", llm_config.get("base_url", "")).strip().rstrip("/")
        self.model_name = os.getenv(f"{self.provider.upper()}_MODEL", llm_config.get("model_name", "default-model"))
        self.api_key = os.getenv("LLM_API_KEY", llm_config.get("api_key", None))
        self.max_retries = 3

        # ✅ Fix for Podman/Openshift localhost issue
        if self.base_url == "http://localhost:8000":
            self.base_url = "http://host.containers.internal:8000"

        logger.info(f"✅ Using Provider: {self.provider} | Model: {self.model_name} | URL: {self.base_url}")

        if not self.base_url:
            logger.error("❌ LLM Base URL is missing. Check OpenShift ConfigMap or environment variables.")
        if not self.api_key and self.provider not in ["mistral", "ollama", "vllm", "deepseek"]:
            logger.warning("⚠️ No LLM API Key provided. Some endpoints may require authentication.")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No LLM API URL configured.")
            return json.dumps({"error": "Missing LLM API URL in config"})

        # ✅ Define API endpoint based on provider
        if self.provider == "vllm":
            url = f"{self.base_url}/v1/completions"
            payload = {"model": self.model_name, "prompt": prompt, "temperature": 0.1, "max_tokens": 1000}
        elif self.provider == "ollama":
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif self.provider == "gemini":
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        elif self.provider == "deepseek":
            url = f"{self.base_url}/chat/completions"
            payload = {"model": self.model_name, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        elif self.provider == "granite":
            url = f"{self.base_url}/v1/chat/completions"
            payload = {"model": self.model_name, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        else:  # Default: OpenAI-compatible APIs
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Respond in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
            }

        # ✅ Use API key if required
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}

        # ✅ Retry mechanism for API failures
        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = datetime.now()
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()

                elapsed_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"⏱️ LLM API Response Time: {elapsed_time:.2f} seconds")

                logger.info(f"✅ Raw LLM API Response: {json.dumps(data, indent=2)}")

                # ✅ Fix: Parse response correctly based on API structure
                if self.provider in ["vllm", "ollama"]:
                    return json.dumps({"text": data["choices"][0]["text"].strip()}, indent=2)

                choices = data.get("choices", [])
                if choices:
                    response_text = choices[0].get("message", {}).get("content", "").strip()
                    json_part = extract_json(response_text)
                    return json.dumps(json.loads(json_part), indent=2) if json_part else json.dumps({"error": "Invalid JSON received"})

                return json.dumps({"error": "Empty response from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep(5)
                    logger.info(f"🔄 Retrying... Attempt {attempt + 1}/{self.max_retries}")
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
