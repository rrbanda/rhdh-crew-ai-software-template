"""
LlamaStack LLM Configuration for CrewAI

This module configures the LLM connection to LlamaStack's OpenAI-compatible API
using environment variables that CrewAI/LiteLLM understands.
"""

import os
import logging

logger = logging.getLogger(__name__)

# LlamaStack Configuration
LLAMASTACK_BASE_URL = os.getenv(
    "LLAMASTACK_BASE_URL",
    "https://lss-lss.apps.cluster-nngf2.dynamic.redhatworkshops.io/v1"
)
LLAMASTACK_MODEL = os.getenv(
    "LLAMASTACK_MODEL",
    "remote-llm/llama-4-scout-17b-16e-w4a16"
)
LLAMASTACK_API_KEY = os.getenv("LLAMASTACK_API_KEY", "not-needed")


def configure_llm_environment():
    """
    Configure environment variables for CrewAI to use LlamaStack.
    
    CrewAI uses LiteLLM under the hood, which respects OpenAI environment variables.
    By setting these, we can use LlamaStack without explicit LLM class configuration.
    """
    # Set OpenAI-compatible environment variables
    os.environ["OPENAI_API_BASE"] = LLAMASTACK_BASE_URL
    os.environ["OPENAI_API_KEY"] = LLAMASTACK_API_KEY
    
    logger.info(f"🔗 Configured LlamaStack: {LLAMASTACK_BASE_URL}")
    logger.info(f"📦 Default model: {LLAMASTACK_MODEL}")


def get_model_name() -> str:
    """
    Get the model name to use with CrewAI agents.
    
    For OpenAI-compatible endpoints, we prefix with 'openai/' 
    to tell LiteLLM to use the OpenAI provider.
    """
    return f"openai/{LLAMASTACK_MODEL}"


def get_available_models() -> list:
    """
    Fetch available models from LlamaStack.
    Useful for debugging and model selection.
    """
    import requests
    
    try:
        # Remove /v1 suffix for models endpoint
        base = LLAMASTACK_BASE_URL.rstrip('/v1').rstrip('/')
        response = requests.get(
            f"{base}/v1/models",
            headers={"accept": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Filter for LLM models only
        llm_models = [
            m["identifier"] for m in data.get("data", [])
            if m.get("model_type") == "llm"
        ]
        return llm_models
    except Exception as e:
        logger.error(f"❌ Failed to fetch models: {e}")
        return []


# Configure on import
configure_llm_environment()
