"""
Utility functions for the Leopard Pont des Arts application.
"""

import yaml
import os
import logging

logger = logging.getLogger(__name__)

# Configuration paths
CONFIG_DIR = os.getenv("CONFIG_DIR", "configs")


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary containing the YAML contents
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with open(file_path, "r") as file:
        return yaml.safe_load(file) or {}


def load_config() -> dict:
    """Load application configuration from config.yaml."""
    config_path = os.path.join(CONFIG_DIR, "config.yaml")
    try:
        return load_yaml(config_path)
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return {}


def load_agents_config() -> dict:
    """Load agent configurations from agents.yaml."""
    agents_path = os.path.join(CONFIG_DIR, "agents.yaml")
    try:
        return load_yaml(agents_path)
    except FileNotFoundError:
        logger.warning(f"Agents config not found: {agents_path}, using defaults")
        return {}


def load_tasks_config() -> dict:
    """Load task configurations from tasks.yaml."""
    tasks_path = os.path.join(CONFIG_DIR, "tasks.yaml")
    try:
        return load_yaml(tasks_path)
    except FileNotFoundError:
        logger.warning(f"Tasks config not found: {tasks_path}, using defaults")
        return {}
