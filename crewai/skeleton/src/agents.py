"""
CrewAI Agents for Leopard Pont des Arts Calculator

This module defines proper CrewAI agents that leverage the framework's
reasoning capabilities, tool usage, and LLM integration.
"""

import os
import yaml
import logging
from crewai import Agent
from crewai.tools import tool
from src.llm import get_model_name

logger = logging.getLogger(__name__)

# Load Agent Configuration from YAML
CONFIG_DIR = os.getenv("CONFIG_DIR", "configs")

try:
    with open(f"{CONFIG_DIR}/agents.yaml", "r") as file:
        agent_configs = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logger.warning(f"⚠️ Agent config not found, using defaults: {e}")
    agent_configs = {}


@tool("Web Search")
def web_search(query: str) -> str:
    """
    Search the internet for current information about animals, distances, 
    speeds, landmarks, bridges, and other factual data.
    
    Args:
        query: The search query string to look up
        
    Returns:
        Search results as a string
    """
    from duckduckgo_search import DDGS
    
    logger.info(f"🔍 Searching for: {query}")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            
        if not results:
            return "No results found."
            
        # Format results
        formatted = []
        for r in results:
            formatted.append(f"- {r.get('title', 'No title')}: {r.get('body', 'No description')}")
        
        return "\n".join(formatted)
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        return f"Search failed: {str(e)}"


def create_leopard_researcher() -> Agent:
    """
    Create a researcher agent that gathers factual information.
    
    This agent uses web search to find accurate data about:
    - Leopard running speeds
    - Bridge dimensions
    - Other relevant facts
    """
    config = agent_configs.get("researcher", {})
    model_name = get_model_name()
    
    logger.info(f"🔬 Creating Researcher agent with model: {model_name}")
    
    return Agent(
        role=config.get("role", "Wildlife & Geography Researcher"),
        goal=config.get("goal", "Find accurate factual information about animals and landmarks"),
        backstory=config.get("backstory", (
            "You are an expert researcher specializing in wildlife biology and geography. "
            "You excel at finding accurate, up-to-date information from reliable sources. "
            "You always verify facts before reporting them."
        )),
        llm=model_name,
        tools=[web_search],
        verbose=True,
        allow_delegation=False
    )


def create_leopard_calculator() -> Agent:
    """
    Create a calculator agent that performs computations.
    
    This agent takes factual data and performs mathematical
    calculations to answer the crossing time question.
    """
    config = agent_configs.get("calculator", {})
    model_name = get_model_name()
    
    logger.info(f"🧮 Creating Calculator agent with model: {model_name}")
    
    return Agent(
        role=config.get("role", "Physics Calculator"),
        goal=config.get("goal", "Calculate precise time measurements using physics formulas"),
        backstory=config.get("backstory", (
            "You are a physicist who specializes in motion calculations. "
            "Given speed and distance, you calculate time with precision. "
            "You always show your work and use the formula: Time = Distance / Speed. "
            "You convert units carefully (km/h to m/s by dividing by 3.6)."
        )),
        llm=model_name,
        tools=[],  # Calculator doesn't need search - it gets facts from researcher
        verbose=True,
        allow_delegation=False
    )


def get_agents() -> list[Agent]:
    """
    Get all agents for the Leopard Pont des Arts crew.
    Returns a list of agents that work together.
    """
    return [
        create_leopard_researcher(),
        create_leopard_calculator()
    ]
