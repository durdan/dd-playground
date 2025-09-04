from crewai import Crew, Process
from agents.code_agents import CodeGenerationAgents
from tasks.code_tasks import CodeGenerationTasks
from typing import Dict, Any

class CodeGenerationCrew:
    def __init__(self, llm_model="gpt-4"):
        self.agents = CodeGenerationAgents(llm_model)
        self.tasks = CodeGenerationTasks()
        
        # Initialize agents
        self.architect = self.agents.create_architect_agent()
        self.developer = self.agents.create_developer_agent()
        self.reviewer = self.agents.create_reviewer_agent()
        self.tester = self.agents.create_tester_agent()
    
    def generate_code(self, requirements: str) -> Dict[str, Any]:
        """
        Generate code using multi-agent collaboration.
        
        Args:
            requirements: Detailed requirements for the code to generate
            
        Returns:
            Dictionary containing architecture, code, review, and tests
        """
        # Create tasks
        architecture_task = self.tasks.create_architecture_task(
            self.architect, requirements
        )
        
        implementation_task = self.tasks.create_implementation_task(
            self.developer, "{architecture_output}"
        )
        
        review_task = self.tasks.create_review_task(
            self.reviewer, "{implementation_output}"
        )
        
        testing_task = self.tasks.create_testing_task(
            self.tester, "{implementation_output}", "{architecture_output}"
        )
        
        # Set up task dependencies
        implementation_task.context = [architecture_task]
        review_task.context = [implementation_task]
        testing_task.context = [implementation_task, architecture_task]
        
        # Create and run crew
        crew = Crew(
            agents=[self.architect, self.developer, self.reviewer, self.tester],
            tasks=[architecture_task, implementation_task, review_task, testing_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "architecture": architecture_task.output.raw_output,
            "implementation": implementation_task.output.raw_output,
            "review": review_task.output.raw_output,
            "tests": testing_task.output.raw_output,
            "full_result": result
        }
    
    def iterative_improvement(self, requirements: str, iterations: int = 2) -> Dict[str, Any]:
        """
        Generate code with iterative improvement cycles.
        
        Args:
            requirements: Initial requirements
            iterations: Number of improvement iterations
            
        Returns:
            Final improved code generation result
        """
        current_result = self.generate_code(requirements)
        
        for i in range(iterations):
            # Create improvement requirements based on review feedback
            improvement_requirements = f"""
            Original requirements: {requirements}
            
            Previous implementation review feedback:
            {current_result['review']}
            
            Please improve the implementation addressing all review feedback.
            """
            
            current_result = self.generate_code(improvement_requirements)
        
        return current_result