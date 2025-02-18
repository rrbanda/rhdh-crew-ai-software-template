import yaml
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ✅ Go one level up
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")  # ✅ New location!
TASKS_PATH = os.path.join(BASE_DIR, "src", "tasks.yaml")
AGENTS_PATH = os.path.join(BASE_DIR, "src", "agents.yaml")

def load_yaml(file_path):
    """Loads a YAML file and returns its content as a dictionary."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Config file not found: {file_path}")

    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def load_config():
    """Load system-wide configurations from config.yaml."""
    return load_yaml(CONFIG_PATH)

def load_tasks():
    """Load tasks configuration if tasks.yaml is still in use."""
    return load_yaml(TASKS_PATH)

def load_agents():
    """Load agents configuration if agents.yaml is still in use."""
    return load_yaml(AGENTS_PATH)
