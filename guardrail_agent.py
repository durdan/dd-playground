from crewai import Agent, Task as CrewTask, Crew
from models import Task, ValidationResult, ValidationStatus
from config import GuardrailConfig, CrewConfig
from typing import List

class GuardrailAgent:
    def __init__(self):
        self.config = GuardrailConfig()
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        return Agent(
            role="Compliance & Security Guardian",
            goal="Enforce security, compliance, and performance guardrails",
            backstory="""You are a security and compliance expert responsible for 
            ensuring all development tasks meet security standards, compliance 
            requirements, and performance guidelines. You identify risks and 
            enforce organizational policies.""",
            verbose=CrewConfig.VERBOSE,
            allow_delegation=False
        )
    
    def enforce_guardrails(self, task: Task) -> ValidationResult:
        """Enforce guardrails against task"""
        try:
            crew_task = CrewTask(
                description=self._build_guardrail_prompt(task),
                agent=self.agent,
                expected_output="Guardrail enforcement result with violations and recommendations"
            )
            
            crew = Crew(
                agents=[self.agent],
                tasks=[crew_task],
                verbose=CrewConfig.VERBOSE
            )
            
            result = crew.kickoff()
            return self._parse_guardrail_result(result, task)
            
        except Exception as e:
            return ValidationResult(
                agent_name="guardrail",
                status=ValidationStatus.FAILED,
                message=f"Guardrail enforcement failed: {str(e)}",
                details={"error": str(e)}
            )
    
    def _build_guardrail_prompt(self, task: Task) -> str:
        return f"""
        Enforce guardrails for the following task:
        
        Task: {task.title}
        Description: {task.description}
        Type: {task.task_type}
        Proposed Solution: {task.proposed_solution or 'Not provided'}
        
        Security Rules to Check:
        {chr(10).join(f'- {rule}' for rule in self.config.SECURITY_RULES)}
        
        Compliance Rules to Check:
        {chr(10).join(f'- {rule}' for rule in self.config.COMPLIANCE_RULES)}
        
        Performance Rules:
        {chr(10).join(f'- {k}: {v}' for k, v in self.config.PERFORMANCE_RULES.items())}
        
        Identify:
        1. Any violations or risks
        2. Compliance gaps
        3. Security concerns
        4. Performance implications
        
        Provide:
        - Status: PASSED/FAILED/WARNING
        - List of violations found
        - Required actions to comply
        
        Format as: STATUS|violations_summary|required_actions (separated by semicolons)
        """
    
    def _parse_guardrail_result(self, result: str, task: Task) -> ValidationResult:
        """Parse guardrail enforcement result"""
        try:
            parts = str(result).split('|')
            if len(parts) >= 3:
                status_str = parts[0].strip().upper()
                violations = parts[1].strip()
                actions = [a.strip() for a in parts[2].split(';') if a.strip()]
                
                status = ValidationStatus.PASSED
                if status_str == "FAILED":
                    status = ValidationStatus.FAILED
                elif status_str == "WARNING":
                    status = ValidationStatus.WARNING
                
                return ValidationResult(
                    agent_name="guardrail",
                    status=status,
                    message=violations,
                    suggestions=actions,
                    details={"task_type": task.task_type}
                )
            else:
                return ValidationResult(
                    agent_name="guardrail",
                    status=ValidationStatus.WARNING,
                    message="Guardrail check completed with limited parsing",
                    suggestions=["Review compliance manually"],
                    details={"raw_result": str(result)}
                )
                
        except Exception as e:
            return ValidationResult(
                agent_name="guardrail",
                status=ValidationStatus.FAILED,
                message=f"Failed to parse guardrail result: {str(e)}",
                details={"error": str(e), "raw_result": str(result)}
            )