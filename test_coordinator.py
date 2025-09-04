from crewai import Crew
from typing import Dict, Any, Optional
from .test_generator import BaseTestGenerator, TestSuite, TestCase
from .crew_agents import TestCrewAgents
from .crew_tasks import TestCrewTasks
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrewAITestCoordinator:
    """Coordinates test generation using CrewAI agents"""
    
    def __init__(self):
        self.base_generator = BaseTestGenerator()
        self.agents = TestCrewAgents()
        self.tasks = TestCrewTasks()
    
    def generate_coordinated_tests(self, code: str, module_name: str) -> TestSuite:
        """Generate tests using CrewAI coordination"""
        try:
            # Step 1: Analyze code using base generator
            logger.info(f"Analyzing code for module: {module_name}")
            code_analysis = self.base_generator.analyze_code(code)
            
            # Step 2: Create CrewAI agents
            planner = self.agents.create_test_planner()
            writer = self.agents.create_test_writer()
            reviewer = self.agents.create_test_reviewer()
            
            # Step 3: Create tasks
            planning_task = self.tasks.create_planning_task(code_analysis)
            planning_task.agent = planner
            
            # Step 4: Execute planning
            crew = Crew(
                agents=[planner],
                tasks=[planning_task],
                verbose=True
            )
            
            planning_result = crew.kickoff()
            logger.info("Test planning completed")
            
            # Step 5: Generate test code
            writing_task = self.tasks.create_writing_task(str(planning_result))
            writing_task.agent = writer
            
            writing_crew = Crew(
                agents=[writer],
                tasks=[writing_task],
                verbose=True
            )
            
            test_code_result = writing_crew.kickoff()
            logger.info("Test code generation completed")
            
            # Step 6: Review and refine
            review_task = self.tasks.create_review_task(str(test_code_result))
            review_task.agent = reviewer
            
            review_crew = Crew(
                agents=[reviewer],
                tasks=[review_task],
                verbose=True
            )
            
            final_result = review_crew.kickoff()
            logger.info("Test review completed")
            
            # Step 7: Parse and structure results
            test_cases = self._parse_generated_tests(str(final_result), code_analysis)
            
            return TestSuite(
                module_name=module_name,
                test_cases=test_cases,
                coverage_target=0.85
            )
            
        except Exception as e:
            logger.error(f"Error in coordinated test generation: {e}")
            # Fallback to basic generation
            return self._fallback_generation(code, module_name, code_analysis)
    
    def _parse_generated_tests(self, generated_code: str, analysis: Dict[str, Any]) -> List[TestCase]:
        """Parse generated test code into TestCase objects"""
        test_cases = []
        
        # Simple parsing - in production, use AST parsing
        lines = generated_code.split('\n')
        current_test = None
        current_code = []
        
        for line in lines:
            if line.strip().startswith('def test_'):
                if current_test:
                    test_cases.append(TestCase(
                        name=current_test,
                        description=f"Generated test for {current_test}",
                        test_code='\n'.join(current_code),
                        test_type="unit"
                    ))
                
                current_test = line.strip().split('(')[0].replace('def ', '')
                current_code = [line]
            elif current_test and line.strip():
                current_code.append(line)
        
        # Add the last test
        if current_test and current_code:
            test_cases.append(TestCase(
                name=current_test,
                description=f"Generated test for {current_test}",
                test_code='\n'.join(current_code),
                test_type="unit"
            ))
        
        return test_cases if test_cases else self._create_fallback_tests(analysis)
    
    def _create_fallback_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Create basic tests if parsing fails"""
        test_cases = []
        for func in analysis.get('functions', []):
            test_case = self.base_generator.generate_basic_test(func)
            test_cases.append(test_case)
        return test_cases
    
    def _fallback_generation(self, code: str, module_name: str, analysis: Dict[str, Any]) -> TestSuite:
        """Fallback to basic generation if CrewAI fails"""
        logger.warning("Using fallback test generation")
        test_cases = self._create_fallback_tests(analysis)
        return TestSuite(
            module_name=module_name,
            test_cases=test_cases,
            coverage_target=0.7
        )