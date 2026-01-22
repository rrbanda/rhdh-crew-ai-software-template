"""
FastAPI Application for Leopard Pont des Arts Calculator

This API exposes the CrewAI multi-agent system that calculates
how long it takes a leopard to cross the Pont des Arts bridge.
"""

import os
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Crew
from dotenv import load_dotenv

from src.llm import get_available_models, LLAMASTACK_BASE_URL, LLAMASTACK_MODEL
from src.tasks import get_tasks

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Leopard Pont des Arts API",
    description="A CrewAI-powered API that calculates how fast a leopard can cross the Pont des Arts bridge",
    version="2.0.0"
)


class LeopardResult(BaseModel):
    """Response model for leopard crossing calculation"""
    leopard_speed_kmh: float | None = None
    leopard_speed_ms: float | None = None
    bridge_length_meters: float | None = None
    crossing_time_seconds: float | None = None
    calculation: str | None = None
    explanation: str | None = None
    raw_output: str | None = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    llm_url: str
    llm_model: str


class ModelsResponse(BaseModel):
    """Available models response"""
    models: list[str]


@app.get("/", tags=["General"])
def home():
    """Root endpoint with API information."""
    return {
        "message": "Leopard Pont des Arts API is running!",
        "version": "2.0.0",
        "endpoints": {
            "/health": "Health check",
            "/models": "List available LlamaStack models",
            "/leopard-crossing": "Calculate leopard crossing time"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health():
    """Health check endpoint with LLM configuration info."""
    return HealthResponse(
        status="ok",
        llm_url=LLAMASTACK_BASE_URL,
        llm_model=LLAMASTACK_MODEL
    )


@app.get("/models", response_model=ModelsResponse, tags=["General"])
def list_models():
    """List available models from LlamaStack."""
    models = get_available_models()
    return ModelsResponse(models=models)


@app.get("/leopard-crossing", tags=["Calculation"])
def leopard_crossing():
    """
    Calculate how many seconds it takes for a leopard to cross Pont des Arts.
    
    This endpoint triggers a CrewAI crew with two agents:
    1. A Researcher agent that searches for factual data
    2. A Calculator agent that computes the crossing time
    
    The agents collaborate using CrewAI's built-in orchestration.
    """
    try:
        logger.info("🚀 Starting CrewAI execution...")
        
        # Get agents and tasks
        agents, tasks = get_tasks()
        
        # Create the crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True  # Enable detailed logging
        )
        
        # Execute the crew
        logger.info("🐆 Kicking off the Leopard Crossing Crew...")
        result = crew.kickoff()
        
        logger.info(f"✅ Crew execution completed")
        logger.info(f"📄 Raw result: {result}")
        
        # Try to parse as JSON, otherwise return raw
        try:
            if hasattr(result, 'raw'):
                parsed = json.loads(result.raw)
            else:
                parsed = json.loads(str(result))
            return parsed
        except json.JSONDecodeError:
            # Return as raw output if not valid JSON
            return {
                "raw_output": str(result.raw) if hasattr(result, 'raw') else str(result),
                "explanation": "Result was not in JSON format"
            }
            
    except Exception as e:
        logger.error(f"❌ CrewAI execution failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute crew: {str(e)}"
        )


@app.get("/leopard-crossing/simple", tags=["Calculation"])
def leopard_crossing_simple():
    """
    Simplified endpoint that returns just the key metrics.
    
    Returns only the crossing time and a brief explanation.
    """
    result = leopard_crossing()
    
    if "error" in result or "raw_output" in result:
        return result
    
    return {
        "crossing_time_seconds": result.get("crossing_time_seconds"),
        "explanation": result.get("explanation", result.get("calculation"))
    }


# Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
