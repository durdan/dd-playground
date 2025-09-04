import os
from typing import Dict, Any, Optional
from crew.code_generation_crew import CodeGenerationCrew
from dotenv import load_dotenv

class EnhancedCodeGenerator:
    def __init__(self, llm_model: str = "gpt-4"):
        load_dotenv()
        
        # Validate OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.crew = CodeGenerationCrew(llm_model)
    
    def generate_complex_implementation(
        self, 
        requirements: str,
        use_iterative_improvement: bool = True,
        iterations: int = 2
    ) -> Dict[str, Any]:
        """
        Generate complex code implementation using multi-agent collaboration.
        
        Args:
            requirements: Detailed requirements for the implementation
            use_iterative_improvement: Whether to use iterative improvement
            iterations: Number of improvement iterations
            
        Returns:
            Complete code generation result with all components
        """
        if not requirements.strip():
            raise ValueError("Requirements cannot be empty")
        
        try:
            if use_iterative_improvement:
                result = self.crew.iterative_improvement(requirements, iterations)
            else:
                result = self.crew.generate_code(requirements)
            
            return self._format_result(result)
            
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")
    
    def _format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format the result for better usability."""
        return {
            "success": True,
            "architecture": {
                "content": result["architecture"],
                "type": "architecture_design"
            },
            "implementation": {
                "content": result["implementation"],
                "type": "source_code"
            },
            "code_review": {
                "content": result["review"],
                "type": "review_feedback"
            },
            "test_suite": {
                "content": result["tests"],
                "type": "test_code"
            },
            "metadata": {
                "generated_by": "CrewAI Multi-Agent System",
                "agents_used": ["architect", "developer", "reviewer", "tester"]
            }
        }
    
    def save_generated_code(self, result: Dict[str, Any], output_dir: str = "generated_code"):
        """Save generated code to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each component to separate files
        components = {
            "architecture.md": result["architecture"]["content"],
            "implementation.py": result["implementation"]["content"],
            "code_review.md": result["code_review"]["content"],
            "tests.py": result["test_suite"]["content"]
        }
        
        saved_files = []
        for filename, content in components.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files.append(filepath)
        
        return saved_files