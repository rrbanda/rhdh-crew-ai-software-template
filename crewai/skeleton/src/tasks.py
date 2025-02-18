import yaml
import logging
from crewai import Task
from src.agents import LeopardPontDesArtsAgent

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Load Task Configurations
try:
    with open("configs/tasks.yaml", "r") as file:
        task_configs = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logger.error(f"❌ Task config file not found: {e}")
    task_configs = {}

def get_leopard_task():
    """Dynamically retrieves the configured task for the Leopard AI Agent."""
    description = task_configs.get("leopard_task", {}).get("description")
    expected_output = task_configs.get("leopard_task", {}).get("expected_output")

    # ✅ Log a warning if missing fields
    if not description:
        logger.warning("⚠️ Task description missing in tasks.yaml, using default.")
        description = "Analyze the speed of a leopard."

    if not expected_output:
        logger.warning("⚠️ Expected output missing in tasks.yaml, using default.")
        expected_output = "The estimated time for a leopard to run across Pont des Arts."

    # ✅ Initialize task with dynamically loaded agent
    return Task(
        description=description,
        expected_output=expected_output,
        agent=LeopardPontDesArtsAgent()
    )
