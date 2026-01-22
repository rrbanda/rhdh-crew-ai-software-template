"""
CrewAI Tasks for Leopard Pont des Arts Calculator

This module defines the tasks that agents will perform.
Tasks are the work items that drive agent behavior.
"""

import os
import yaml
import logging
from crewai import Task
from src.agents import create_leopard_researcher, create_leopard_calculator

logger = logging.getLogger(__name__)

# Load Task Configuration from YAML
CONFIG_DIR = os.getenv("CONFIG_DIR", "configs")

try:
    with open(f"{CONFIG_DIR}/tasks.yaml", "r") as file:
        task_configs = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logger.warning(f"⚠️ Task config not found, using defaults: {e}")
    task_configs = {}


def create_research_task(researcher) -> Task:
    """
    Create a research task to gather facts about leopards and Pont des Arts.
    
    The researcher agent will use web search to find:
    - Maximum running speed of a leopard
    - Length of the Pont des Arts bridge in Paris
    """
    config = task_configs.get("research_task", {})
    
    return Task(
        description=config.get("description", (
            "Research and find the following factual information:\n"
            "1. What is the maximum running speed of a leopard in km/h?\n"
            "2. What is the length of the Pont des Arts bridge in Paris in meters?\n\n"
            "Use the web search tool to find accurate, current information. "
            "Cite your sources if possible."
        )),
        expected_output=config.get("expected_output", (
            "A clear report containing:\n"
            "- Leopard's maximum speed (in km/h)\n"
            "- Pont des Arts bridge length (in meters)\n"
            "- Sources or reasoning for these values"
        )),
        agent=researcher
    )


def create_calculation_task(calculator, context_tasks: list) -> Task:
    """
    Create a calculation task to compute the crossing time.
    
    The calculator agent receives context from the research task
    and performs the time calculation.
    """
    config = task_configs.get("calculation_task", {})
    
    return Task(
        description=config.get("description", (
            "Using the research data provided, calculate how many seconds "
            "it would take for a leopard running at maximum speed to cross "
            "the Pont des Arts bridge.\n\n"
            "Steps:\n"
            "1. Convert the leopard's speed from km/h to m/s (divide by 3.6)\n"
            "2. Apply the formula: Time (seconds) = Distance (meters) / Speed (m/s)\n"
            "3. Round to 2 decimal places\n\n"
            "Show your calculations clearly."
        )),
        expected_output=config.get("expected_output", (
            "A JSON response with the following structure:\n"
            "{\n"
            '  "leopard_speed_kmh": <number>,\n'
            '  "leopard_speed_ms": <number>,\n'
            '  "bridge_length_meters": <number>,\n'
            '  "crossing_time_seconds": <number>,\n'
            '  "calculation": "<formula and steps>",\n'
            '  "explanation": "<brief explanation>"\n'
            "}"
        )),
        agent=calculator,
        context=context_tasks  # This task receives output from research task
    )


def get_tasks() -> tuple[list, list]:
    """
    Create and return all tasks with their assigned agents.
    
    Returns:
        tuple: (list of agents, list of tasks)
    """
    # Create agents
    researcher = create_leopard_researcher()
    calculator = create_leopard_calculator()
    
    # Create tasks with proper context chain
    research_task = create_research_task(researcher)
    calculation_task = create_calculation_task(calculator, context_tasks=[research_task])
    
    agents = [researcher, calculator]
    tasks = [research_task, calculation_task]
    
    return agents, tasks
