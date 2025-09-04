"""
CrewAI integration package for FDJ CLI.
Provides AI agent orchestration capabilities.
"""

from .core.agent import Agent
from .core.task import Task
from .core.crew import Crew
from .core.tool import Tool

__version__ = "0.1.0"
__all__ = ["Agent", "Task", "Crew", "Tool"]