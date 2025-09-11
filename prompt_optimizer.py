from typing import Dict, Any
from .models import SpecificationType


class PromptOptimizer:
    """Optimizer subagent for efficient prompt engineering."""
    
    def __init__(self):
        self._templates = self._load_templates()
        self._optimization_rules = self._load_optimization_rules()
    
    def optimize_prompt(self, spec_type: SpecificationType, requirements: str, 
                       context: Dict[str, Any] = None) -> str:
        """Optimize prompt for specific specification type."""
        if not requirements.strip():
            raise ValueError("Requirements cannot be empty")
        
        template = self._templates.get(spec_type)
        if not template:
            raise ValueError(f"No template found for {spec_type.value}")
        
        optimized_prompt = self._apply_template(template, requirements, context or {})
        return self._apply_optimization_rules(optimized_prompt, spec_type)
    
    def _load_templates(self) -> Dict[SpecificationType, str]:
        return {
            SpecificationType.BUSINESS_ANALYSIS: """
            Generate a comprehensive business analysis document based on the following requirements:
            
            Requirements: {requirements}
            Context: {context}
            
            Structure the analysis with:
            1. Executive Summary
            2. Business Requirements
            3. Stakeholder Analysis
            4. Risk Assessment
            5. Success Metrics
            6. Implementation Timeline
            
            Be specific, actionable, and data-driven.
            """,
            
            SpecificationType.TEST_SPECS: """
            Create detailed test specifications for the following requirements:
            
            Requirements: {requirements}
            Context: {context}
            
            Include:
            1. Test Objectives
            2. Test Scenarios (positive/negative/edge cases)
            3. Test Data Requirements
            4. Acceptance Criteria
            5. Performance Benchmarks
            6. Test Environment Setup
            
            Focus on comprehensive coverage and clear pass/fail criteria.
            """,
            
            SpecificationType.ARCHITECTURE_SPECS: """
            Design comprehensive architecture specifications for:
            
            Requirements: {requirements}
            Context: {context}
            
            Provide:
            1. System Architecture Overview
            2. Component Design
            3. Data Flow Diagrams
            4. Technology Stack Recommendations
            5. Scalability Considerations
            6. Security Architecture
            7. Integration Points
            
            Emphasize scalability, maintainability, and best practices.
            """
        }
    
    def _load_optimization_rules(self) -> Dict[SpecificationType, Dict[str, Any]]:
        return {
            SpecificationType.BUSINESS_ANALYSIS: {
                "max_tokens": 2000,
                "temperature": 0.3,
                "focus_keywords": ["ROI", "stakeholders", "metrics", "timeline"]
            },
            SpecificationType.TEST_SPECS: {
                "max_tokens": 1500,
                "temperature": 0.2,
                "focus_keywords": ["test cases", "coverage", "criteria", "validation"]
            },
            SpecificationType.ARCHITECTURE_SPECS: {
                "max_tokens": 2500,
                "temperature": 0.4,
                "focus_keywords": ["scalability", "patterns", "components", "integration"]
            }
        }
    
    def _apply_template(self, template: str, requirements: str, 
                       context: Dict[str, Any]) -> str:
        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()]) if context else "None provided"
        return template.format(requirements=requirements, context=context_str).strip()
    
    def _apply_optimization_rules(self, prompt: str, spec_type: SpecificationType) -> str:
        rules = self._optimization_rules.get(spec_type, {})
        focus_keywords = rules.get("focus_keywords", [])
        
        if focus_keywords:
            emphasis = f"\n\nPay special attention to: {', '.join(focus_keywords)}"
            prompt += emphasis
        
        return prompt
    
    def get_generation_params(self, spec_type: SpecificationType) -> Dict[str, Any]:
        """Get optimized parameters for LLM generation."""
        rules = self._optimization_rules.get(spec_type, {})
        return {
            "max_tokens": rules.get("max_tokens", 2000),
            "temperature": rules.get("temperature", 0.3),
        }