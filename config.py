from typing import Dict, List

class ArchitectConfig:
    DESIGN_PRINCIPLES = [
        "Follow SOLID principles",
        "Maintain separation of concerns",
        "Ensure proper abstraction layers",
        "Consider scalability and maintainability",
        "Follow established patterns and conventions"
    ]
    
    ARCHITECTURE_RULES = {
        "max_complexity": 10,
        "required_documentation": True,
        "dependency_injection": True,
        "error_handling": True
    }

class GuardrailConfig:
    SECURITY_RULES = [
        "No hardcoded credentials",
        "Input validation required",
        "Proper authentication/authorization",
        "Secure data handling"
    ]
    
    COMPLIANCE_RULES = [
        "Code review required",
        "Testing coverage > 80%",
        "Documentation updated",
        "Breaking changes documented"
    ]
    
    PERFORMANCE_RULES = {
        "max_response_time": "2s",
        "memory_usage": "reasonable",
        "database_queries": "optimized"
    }

class CrewConfig:
    OPENAI_MODEL = "gpt-4"
    MAX_ITERATIONS = 3
    VERBOSE = True