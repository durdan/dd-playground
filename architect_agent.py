from crewai import Agent, Task as CrewTask, Crew
from models import Task, ValidationResult, ValidationStatus
from config import ArchitectConfig, CrewConfig
from typing import Dict, Any

class ArchitectAgent:
    def __init__(self):
        self.config = ArchitectConfig()
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        return Agent(
            role="Software Architect",
            goal="Validate software design and architecture decisions",
            backstory="""You are an experienced software architect responsible for 
            ensuring that all development tasks follow sound architectural principles 
            and design patterns. You review proposed solutions for maintainability, 
            scalability, and adherence to best practices.""",
            verbose=CrewConfig.VERBOSE,
            allow_delegation=False
        )
    
    def validate_architecture(self, task: Task) -> ValidationResult:
        """Validate task against architectural principles"""
        try:
            crew_task = CrewTask(
                description=self._build_validation_prompt(task),
                agent=self.agent,
                expected_output="Structured validation result with status and recommendations"
            )
            
            crew = Crew(
                agents=[self.agent],
                tasks=[crew_task],
                verbose=CrewConfig.VERBOSE
            )
            
            result = crew.kickoff()
            return self._parse_result(result, task)
            
        except Exception as e:
            return ValidationResult(
                agent_name="architect",
                status=ValidationStatus.FAILED,
                message=f"Architecture validation failed: {str(e)}",
                details={"error": str(e)}
            )
    
    def _build_validation_prompt(self, task: Task) -> str:
        return f"""
        Validate the following task against architectural principles:
        
        Task: {task.title}
        Description: {task.description}
        Type: {task.task_type}
        Requirements: {', '.join(task.requirements)}
        Proposed Solution: {task.proposed_solution or 'Not provided'}
        
        Evaluate against these principles:
        {chr(10).join(f'- {principle}' for principle in self.config.DESIGN_PRINCIPLES)}
        
        Architecture Rules:
        {chr(10).join(f'- {k}: {v}' for k, v in self.config.ARCHITECTURE_RULES.items())}
        
        Provide:
        1. Status: PASSED/FAILED/WARNING
        2. Main concerns or validation points
        3. Specific recommendations for improvement
        4. Risk assessment
        
        Format as: STATUS|message|recommendations (separated by semicolons)
        """
    
    def _parse_result(self, result: str, task: Task) -> ValidationResult:
        """Parse CrewAI result into ValidationResult"""
        try:
            parts = str(result).split('|')
            if len(parts) >= 3:
                status_str = parts[0].strip().upper()
                message = parts[1].strip()
                recommendations = [r.strip() for r in parts[2].split(';') if r.strip()]
                
                status = ValidationStatus.PASSED
                if status_str == "FAILED":
                    status = ValidationStatus.FAILED
                elif status_str == "WARNING":
                    status = ValidationStatus.WARNING
                
                return ValidationResult(
                    agent_name="architect",
                    status=status,
                    message=message,
                    suggestions=recommendations,
                    details={"task_type": task.task_type}
                )
            else:
                # Fallback parsing
                return ValidationResult(
                    agent_name="architect",
                    status=ValidationStatus.WARNING,
                    message="Architecture review completed with limited parsing",
                    suggestions=["Review architectural compliance manually"],
                    details={"raw_result": str(result)}
                )
                
        except Exception as e:
            return ValidationResult(
                agent_name="architect",
                status=ValidationStatus.FAILED,
                message=f"Failed to parse architecture validation: {str(e)}",
                details={"error": str(e), "raw_result": str(result)}
            )