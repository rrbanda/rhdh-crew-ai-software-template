"""
Leopard Pont des Arts - CrewAI Application

A multi-agent AI system that calculates how fast a leopard
can cross the Pont des Arts bridge in Paris.

Run with: python app.py
Or: uvicorn src.api:app --reload
"""

from src.api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
