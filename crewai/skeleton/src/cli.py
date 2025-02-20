import logging
import json
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
    run_crew()
