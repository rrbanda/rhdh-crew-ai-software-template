import logging
import json
import uvicorn
import argparse
from crewai import Crew
from src.tasks import get_leopard_task

logging.basicConfig(level=logging.INFO)

def run_crew():
    """Run the CrewAI agent in CLI mode."""
    task = get_leopard_task()
    crew = Crew(agents=[task.agent], tasks=[task], verbose=True)

    result = crew.kickoff()
    try:
        final_result = json.loads(result.raw) if hasattr(result, "raw") else {"error": "Unexpected response"}
    except json.JSONDecodeError:
        final_result = {"error": "Invalid JSON response"}

    print("\n=== FINAL CREW RESULT ===")
    print(json.dumps(final_result, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cli", "api"], default="cli", help="Run mode: cli (default) or api")
    args = parser.parse_args()

    if args.mode == "api":
        uvicorn.run("src.api:app", host="0.0.0.0", port=8000)
    else:
        run_crew()
