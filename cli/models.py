from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class CrewStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Agent:
    name: str
    role: str
    goal: str


@dataclass
class Task:
    name: str
    description: str
    agent: str
    dependencies: List[str]


@dataclass
class Crew:
    name: str
    agents: List[Agent]
    tasks: List[Task]
    
    
@dataclass
class CrewExecution:
    crew_name: str
    status: CrewStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None