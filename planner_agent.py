from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta

try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Fallback classes for when CrewAI is not available
    class Agent:
        def __init__(self, **kwargs): pass
    class Task:
        def __init__(self, **kwargs): pass
    class Crew:
        def __init__(self, **kwargs): pass
    class Process:
        sequential = "sequential"
        hierarchical = "hierarchical"

logger = logging.getLogger(__name__)

class PlanningComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PlanningTask:
    id: str
    description: str
    complexity: PlanningComplexity
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: timedelta = field(default=timedelta(hours=1))
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class CrewConfig:
    max_agents: int = 5
    process_type: str = "sequential"
    verbose: bool = True
    memory: bool = True
    max_execution_time: int = 300  # seconds

class TaskValidator:
    """Validates and prioritizes planning tasks"""
    
    def validate_task(self, task: PlanningTask) -> bool:
        """Validate a single planning task"""
        if not task.id or not task.description:
            raise ValueError("Task must have id and description")
        
        if task.priority < 1 or task.priority > 10:
            raise ValueError("Task priority must be between 1 and 10")
        
        return True
    
    def resolve_dependencies(self, tasks: List[PlanningTask]) -> List[PlanningTask]:
        """Sort tasks by dependencies and priority"""
        task_map = {task.id: task for task in tasks}
        resolved = []
        visited = set()
        
        def visit(task_id: str):
            if task_id in visited:
                return
            
            task = task_map.get(task_id)
            if not task:
                raise ValueError(f"Dependency task {task_id} not found")
            
            # Visit dependencies first
            for dep_id in task.dependencies:
                visit(dep_id)
            
            visited.add(task_id)
            resolved.append(task)
        
        # Visit all tasks
        for task in tasks:
            visit(task.id)
        
        # Sort by priority within dependency order
        return sorted(resolved, key=lambda t: (len([r for r in resolved[:resolved.index(t)]]), -t.priority))

class TaskCoordinator:
    """Manages task distribution and crew coordination"""
    
    def __init__(self, config: CrewConfig):
        self.config = config
        self.active_tasks: Dict[str, PlanningTask] = {}
        self.completed_tasks: Dict[str, PlanningTask] = {}
        
    def assign_task(self, task: PlanningTask, agent_role: str) -> bool:
        """Assign a task to a specific agent role"""
        if task.id in self.active_tasks:
            logger.warning(f"Task {task.id} is already active")
            return False
        
        task.assigned_agent = agent_role
        task.status = TaskStatus.IN_PROGRESS
        self.active_tasks[task.id] = task
        logger.info(f"Assigned task {task.id} to {agent_role}")
        return True
    
    def complete_task(self, task_id: str, result: Dict[str, Any]) -> bool:
        """Mark a task as completed with results"""
        if task_id not in self.active_tasks:
            logger.error(f"Task {task_id} not found in active tasks")
            return False
        
        task = self.active_tasks.pop(task_id)
        task.status = TaskStatus.COMPLETED
        task.result = result
        self.completed_tasks[task_id] = task
        logger.info(f"Completed task {task_id}")
        return True
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the current status of a task"""
        if task_id in self.active_tasks:
            return self.active_tasks[task_id].status
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id].status
        return None

class PlanningCrew:
    """Wrapper for CrewAI crew management"""
    
    def __init__(self, config: CrewConfig):
        self.config = config
        self.agents: List[Agent] = []
        self.crew: Optional[Crew] = None
        
        if not CREWAI_AVAILABLE:
            logger.warning("CrewAI not available, using fallback mode")
    
    def create_planning_agents(self) -> List[Agent]:
        """Create specialized planning agents"""
        if not CREWAI_AVAILABLE:
            return []
        
        agents = [
            Agent(
                role="Strategic Planner",
                goal="Create high-level strategic plans and identify key objectives",
                backstory="Expert in strategic planning with experience in complex project coordination",
                verbose=self.config.verbose,
                allow_delegation=True
            ),
            Agent(
                role="Task Analyzer",
                goal="Break down complex tasks into manageable components",
                backstory="Specialist in task decomposition and workflow optimization",
                verbose=self.config.verbose,
                allow_delegation=False
            ),
            Agent(
                role="Resource Coordinator",
                goal="Identify and allocate resources efficiently",
                backstory="Expert in resource management and capacity planning",
                verbose=self.config.verbose,
                allow_delegation=False
            ),
            Agent(
                role="Risk Assessor",
                goal="Identify potential risks and create mitigation strategies",
                backstory="Risk management specialist with predictive analysis skills",
                verbose=self.config.verbose,
                allow_delegation=False
            )
        ]
        
        self.agents = agents[:self.config.max_agents]
        return self.agents
    
    def create_crew(self, tasks: List[Task]) -> Optional[Crew]:
        """Create a CrewAI crew with agents and tasks"""
        if not CREWAI_AVAILABLE or not self.agents:
            return None
        
        process = Process.hierarchical if self.config.process_type == "hierarchical" else Process.sequential
        
        self.crew = Crew(
            agents=self.agents,
            tasks=tasks,
            process=process,
            verbose=self.config.verbose,
            memory=self.config.memory
        )
        
        return self.crew

class PlanExecutor:
    """Executes coordinated plans with multiple agents"""
    
    def __init__(self, coordinator: TaskCoordinator, crew: PlanningCrew):
        self.coordinator = coordinator
        self.crew = crew
        self.execution_results: Dict[str, Any] = {}
    
    def execute_plan(self, tasks: List[PlanningTask]) -> Dict[str, Any]:
        """Execute a coordinated plan using the crew"""
        if not CREWAI_AVAILABLE:
            return self._execute_fallback(tasks)
        
        # Convert planning tasks to CrewAI tasks
        crew_tasks = self._convert_to_crew_tasks(tasks)
        
        # Create and execute crew
        crew = self.crew.create_crew(crew_tasks)
        if not crew:
            return self._execute_fallback(tasks)
        
        try:
            result = crew.kickoff()
            self.execution_results = {
                "status": "completed",
                "result": result,
                "tasks_completed": len(tasks),
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            self.execution_results = {
                "status": "failed",
                "error": str(e),
                "tasks_completed": 0,
                "execution_time": datetime.now().isoformat()
            }
        
        return self.execution_results
    
    def _convert_to_crew_tasks(self, planning_tasks: List[PlanningTask]) -> List[Task]:
        """Convert planning tasks to CrewAI tasks"""
        if not CREWAI_AVAILABLE:
            return []
        
        crew_tasks = []
        agent_map = {
            PlanningComplexity.SIMPLE: "Task Analyzer",
            PlanningComplexity.MODERATE: "Strategic Planner", 
            PlanningComplexity.COMPLEX: "Strategic Planner"
        }
        
        for task in planning_tasks:
            agent_role = agent_map.get(task.complexity, "Task Analyzer")
            agent = next((a for a in self.crew.agents if a.role == agent_role), self.crew.agents[0])
            
            crew_task = Task(
                description=task.description,
                agent=agent,
                expected_output=f"Detailed plan for: {task.description}"
            )
            crew_tasks.append(crew_task)
        
        return crew_tasks
    
    def _execute_fallback(self, tasks: List[PlanningTask]) -> Dict[str, Any]:
        """Fallback execution when CrewAI is not available"""
        logger.info("Executing tasks in fallback mode")
        
        completed = 0
        for task in tasks:
            # Simulate task execution
            self.coordinator.assign_task(task, "fallback_agent")
            result = {
                "task_id": task.id,
                "description": task.description,
                "complexity": task.complexity.value,
                "simulated_result": f"Completed {task.description} in fallback mode"
            }
            self.coordinator.complete_task(task.id, result)
            completed += 1
        
        return {
            "status": "completed_fallback",
            "tasks_completed": completed,
            "execution_time": datetime.now().isoformat(),
            "note": "Executed in fallback mode without CrewAI"
        }

class PlannerAgent:
    """Enhanced planner agent with CrewAI coordination capabilities"""
    
    def __init__(self, config: Optional[CrewConfig] = None):
        self.config = config or CrewConfig()
        self.validator = TaskValidator()
        self.coordinator = TaskCoordinator(self.config)
        self.crew = PlanningCrew(self.config)
        self.executor = PlanExecutor(self.coordinator, self.crew)
        
        # Initialize crew agents
        self.crew.create_planning_agents()
        
        logger.info(f"PlannerAgent initialized with CrewAI {'enabled' if CREWAI_AVAILABLE else 'disabled'}")
    
    def create_plan(self, objectives: List[str], complexity: PlanningComplexity = PlanningComplexity.MODERATE) -> List[PlanningTask]:
        """Create a coordinated plan from objectives"""
        if not objectives:
            raise ValueError("Objectives cannot be empty")
        
        tasks = []
        for i, objective in enumerate(objectives):
            task = PlanningTask(
                id=f"task_{i+1}",
                description=objective,
                complexity=complexity,
                priority=len(objectives) - i  # Higher priority for earlier objectives
            )
            self.validator.validate_task(task)
            tasks.append(task)
        
        # Resolve dependencies and return ordered tasks
        return self.validator.resolve_dependencies(tasks)
    
    def execute_coordinated_plan(self, objectives: List[str], complexity: PlanningComplexity = PlanningComplexity.MODERATE) -> Dict[str, Any]:
        """Create and execute a coordinated plan"""
        try:
            # Create plan
            tasks = self.create_plan(objectives, complexity)
            logger.info(f"Created plan with {len(tasks)} tasks")
            
            # Execute plan
            results = self.executor.execute_plan(tasks)
            
            return {
                "plan_created": True,
                "tasks_count": len(tasks),
                "execution_results": results,
                "crew_enabled": CREWAI_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"Plan execution failed: {e}")
            return {
                "plan_created": False,
                "error": str(e),
                "crew_enabled": CREWAI_AVAILABLE
            }
    
    def get_plan_status(self) -> Dict[str, Any]:
        """Get current status of all plans and tasks"""
        return {
            "active_tasks": len(self.coordinator.active_tasks),
            "completed_tasks": len(self.coordinator.completed_tasks),
            "crew_agents": len(self.crew.agents),
            "last_execution": self.executor.execution_results.get("execution_time"),
            "crewai_available": CREWAI_AVAILABLE
        }