from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlanningPhase(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    STRATEGY = "strategy"
    EXECUTION = "execution"

@dataclass
class PlanningContext:
    """Context shared across all planning agents"""
    objective: str
    constraints: List[str]
    resources: Dict[str, Any]
    timeline: str
    stakeholders: List[str]
    
class TaskCoordinator:
    """Manages task dependencies and execution flow"""
    
    def __init__(self):
        self.task_dependencies = {}
        self.completed_tasks = set()
    
    def add_dependency(self, task_id: str, depends_on: List[str]):
        """Add task dependencies"""
        if not task_id or not isinstance(depends_on, list):
            raise ValueError("Invalid task_id or dependencies")
        self.task_dependencies[task_id] = depends_on
    
    def can_execute(self, task_id: str) -> bool:
        """Check if task can be executed based on dependencies"""
        dependencies = self.task_dependencies.get(task_id, [])
        return all(dep in self.completed_tasks for dep in dependencies)
    
    def mark_completed(self, task_id: str):
        """Mark task as completed"""
        self.completed_tasks.add(task_id)

class ResultAggregator:
    """Combines outputs from multiple agents into cohesive plans"""
    
    @staticmethod
    def aggregate_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results from different planning phases"""
        if not results:
            raise ValueError("No results to aggregate")
        
        return {
            "research_insights": results.get("research", {}),
            "analysis_findings": results.get("analysis", {}),
            "strategic_recommendations": results.get("strategy", {}),
            "execution_plan": results.get("execution", {}),
            "integrated_plan": ResultAggregator._create_integrated_plan(results)
        }
    
    @staticmethod
    def _create_integrated_plan(results: Dict[str, Any]) -> Dict[str, Any]:
        """Create an integrated plan from all phases"""
        return {
            "summary": "Integrated planning results",
            "key_insights": results.get("research", {}).get("insights", []),
            "critical_factors": results.get("analysis", {}).get("factors", []),
            "recommended_actions": results.get("strategy", {}).get("actions", []),
            "implementation_steps": results.get("execution", {}).get("steps", [])
        }

class SpecializedAgents:
    """Factory for creating specialized planning agents"""
    
    @staticmethod
    def create_research_agent() -> Agent:
        """Create research specialist agent"""
        return Agent(
            role="Research Specialist",
            goal="Gather comprehensive information and insights relevant to the planning objective",
            backstory="Expert researcher with deep analytical skills and access to diverse information sources",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_analysis_agent() -> Agent:
        """Create analysis specialist agent"""
        return Agent(
            role="Analysis Specialist", 
            goal="Analyze gathered information to identify patterns, risks, and opportunities",
            backstory="Strategic analyst with expertise in data interpretation and risk assessment",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_strategy_agent() -> Agent:
        """Create strategy specialist agent"""
        return Agent(
            role="Strategy Specialist",
            goal="Develop strategic recommendations based on research and analysis",
            backstory="Strategic planning expert with experience in complex decision-making scenarios",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_execution_agent() -> Agent:
        """Create execution specialist agent"""
        return Agent(
            role="Execution Specialist",
            goal="Create detailed implementation plans with timelines and resource allocation",
            backstory="Project management expert specializing in complex plan execution",
            verbose=True,
            allow_delegation=False
        )

class PlanningWorkflow:
    """Defines the multi-agent workflow for complex planning scenarios"""
    
    def __init__(self, context: PlanningContext):
        if not context or not context.objective:
            raise ValueError("Valid planning context required")
        self.context = context
        self.coordinator = TaskCoordinator()
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """Setup task dependencies"""
        self.coordinator.add_dependency("analysis", ["research"])
        self.coordinator.add_dependency("strategy", ["research", "analysis"])
        self.coordinator.add_dependency("execution", ["strategy"])
    
    def create_tasks(self) -> List[Task]:
        """Create tasks for each planning phase"""
        tasks = []
        
        # Research Task
        research_task = Task(
            description=f"""
            Conduct comprehensive research for: {self.context.objective}
            
            Consider:
            - Constraints: {', '.join(self.context.constraints)}
            - Available resources: {self.context.resources}
            - Timeline: {self.context.timeline}
            - Stakeholders: {', '.join(self.context.stakeholders)}
            
            Provide detailed insights and relevant information.
            """,
            agent=SpecializedAgents.create_research_agent(),
            expected_output="Comprehensive research report with key insights and findings"
        )
        tasks.append(research_task)
        
        # Analysis Task
        analysis_task = Task(
            description=f"""
            Analyze the research findings for: {self.context.objective}
            
            Focus on:
            - Identifying critical success factors
            - Risk assessment and mitigation strategies
            - Opportunity analysis
            - Stakeholder impact assessment
            
            Base analysis on the research findings from the previous task.
            """,
            agent=SpecializedAgents.create_analysis_agent(),
            expected_output="Detailed analysis report with risks, opportunities, and critical factors"
        )
        tasks.append(analysis_task)
        
        # Strategy Task
        strategy_task = Task(
            description=f"""
            Develop strategic recommendations for: {self.context.objective}
            
            Create:
            - Strategic options and alternatives
            - Recommended approach with rationale
            - Success metrics and KPIs
            - Resource allocation strategy
            
            Base recommendations on research insights and analysis findings.
            """,
            agent=SpecializedAgents.create_strategy_agent(),
            expected_output="Strategic plan with recommendations, alternatives, and success metrics"
        )
        tasks.append(strategy_task)
        
        # Execution Task
        execution_task = Task(
            description=f"""
            Create detailed execution plan for: {self.context.objective}
            
            Include:
            - Step-by-step implementation timeline
            - Resource requirements and allocation
            - Milestone definitions and checkpoints
            - Risk mitigation actions
            - Communication and reporting structure
            
            Base the plan on the strategic recommendations.
            """,
            agent=SpecializedAgents.create_execution_agent(),
            expected_output="Comprehensive execution plan with timelines, resources, and milestones"
        )
        tasks.append(execution_task)
        
        return tasks

class PlannerAgent:
    """Main orchestrator for coordinating multiple CrewAI agents in complex planning scenarios"""
    
    def __init__(self):
        self.workflows = {}
        self.results_history = []
    
    def create_planning_workflow(self, context: PlanningContext) -> str:
        """Create a new planning workflow"""
        if not context:
            raise ValueError("Planning context is required")
        
        workflow_id = f"workflow_{len(self.workflows) + 1}"
        self.workflows[workflow_id] = PlanningWorkflow(context)
        logger.info(f"Created planning workflow: {workflow_id}")
        return workflow_id
    
    def execute_planning(self, workflow_id: str) -> Dict[str, Any]:
        """Execute the planning workflow with multiple coordinated agents"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        tasks = workflow.create_tasks()
        
        # Create crew with all agents
        crew = Crew(
            agents=[task.agent for task in tasks],
            tasks=tasks,
            process=Process.sequential,  # Sequential execution for dependencies
            verbose=True
        )
        
        logger.info(f"Executing planning workflow: {workflow_id}")
        
        try:
            # Execute the crew
            result = crew.kickoff()
            
            # Process and aggregate results
            processed_results = self._process_crew_results(result, tasks)
            aggregated_results = ResultAggregator.aggregate_results(processed_results)
            
            # Store results
            self.results_history.append({
                "workflow_id": workflow_id,
                "context": workflow.context,
                "results": aggregated_results,
                "timestamp": "2024-01-01"  # In real implementation, use datetime
            })
            
            logger.info(f"Completed planning workflow: {workflow_id}")
            return aggregated_results
            
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
            raise
    
    def _process_crew_results(self, crew_result: Any, tasks: List[Task]) -> Dict[str, Any]:
        """Process results from crew execution"""
        # In a real implementation, this would parse the actual crew results
        # For now, return a structured format based on task phases
        return {
            "research": {"insights": ["Market analysis completed", "Stakeholder needs identified"]},
            "analysis": {"factors": ["Budget constraints", "Timeline pressure", "Resource availability"]},
            "strategy": {"actions": ["Phase 1: Planning", "Phase 2: Implementation", "Phase 3: Review"]},
            "execution": {"steps": ["Step 1: Setup", "Step 2: Execute", "Step 3: Monitor"]}
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a planning workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Find results for this workflow
        workflow_results = next(
            (r for r in self.results_history if r["workflow_id"] == workflow_id),
            None
        )
        
        return {
            "workflow_id": workflow_id,
            "status": "completed" if workflow_results else "pending",
            "context": self.workflows[workflow_id].context,
            "results": workflow_results["results"] if workflow_results else None
        }
    
    def list_workflows(self) -> List[str]:
        """List all created workflows"""
        return list(self.workflows.keys())