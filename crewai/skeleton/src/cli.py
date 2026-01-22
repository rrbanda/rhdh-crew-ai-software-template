"""
CLI Runner for Leopard Pont des Arts CrewAI Agent

Run with: python -m src.cli
"""

import logging
import json
from crewai import Crew
from src.tasks import get_tasks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_crew():
    """Run the CrewAI multi-agent crew in CLI mode."""
    logger.info("🐆 Starting Leopard Pont des Arts Crew...")
    
    # Get agents and tasks
    agents, tasks = get_tasks()
    
    logger.info(f"📋 Loaded {len(agents)} agents and {len(tasks)} tasks")
    for agent in agents:
        logger.info(f"  - Agent: {agent.role}")
    for task in tasks:
        logger.info(f"  - Task: {task.description[:50]}...")
    
    # Create and run the crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )
    
    logger.info("🚀 Kicking off the crew...")
    result = crew.kickoff()
    
    # Parse and display result
    try:
        if hasattr(result, "raw"):
            final_result = json.loads(result.raw)
        else:
            final_result = json.loads(str(result))
    except json.JSONDecodeError:
        final_result = {
            "raw_output": str(result.raw) if hasattr(result, 'raw') else str(result),
            "note": "Result was not in JSON format"
        }

    print("\n" + "=" * 50)
    print("🏁 FINAL CREW RESULT")
    print("=" * 50)
    print(json.dumps(final_result, indent=2))
    print("=" * 50)
    
    return final_result


if __name__ == "__main__":
    run_crew()
