import asyncio
from typing import List, Dict, Any
from test_coordinator import TestRequest, TestResult, TestType

class SubagentManager:
    def __init__(self, subagent_registry: Dict[str, Any]):
        self.subagent_registry = subagent_registry

    async def generate_tests(self, request: TestRequest, test_types: List[TestType]) -> List[TestResult]:
        """Generate tests using existing subagents."""
        tasks = []
        
        for test_type in test_types:
            if test_type.value in self.subagent_registry:
                subagent = self.subagent_registry[test_type.value]
                task = self._execute_subagent(subagent, request, test_type)
                tasks.append(task)
        
        if not tasks:
            return []
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for result in results:
            if isinstance(result, TestResult):
                valid_results.append(result)
        
        return valid_results

    async def _execute_subagent(self, subagent: Any, request: TestRequest, test_type: TestType) -> TestResult:
        """Execute a single subagent and return standardized result."""
        import time
        
        start_time = time.time()
        
        try:
            # Assume subagent has a generate_test method
            test_code = await self._call_subagent_method(subagent, 'generate_test', {
                'code_path': request.code_path,
                'test_type': test_type.value,
                'coverage_threshold': request.coverage_threshold
            })
            
            execution_time = time.time() - start_time
            
            return TestResult(
                agent_name=f"subagent_{test_type.value}",
                test_type=test_type,
                test_code=test_code,
                coverage_info={'estimated_coverage': 0.75},  # Placeholder
                execution_time=execution_time,
                success=True
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                agent_name=f"subagent_{test_type.value}",
                test_type=test_type,
                test_code="",
                coverage_info={},
                execution_time=execution_time,
                success=False,
                errors=[str(e)]
            )

    async def _call_subagent_method(self, subagent: Any, method_name: str, params: Dict[str, Any]) -> str:
        """Call subagent method with proper error handling."""
        if not hasattr(subagent, method_name):
            raise AttributeError(f"Subagent does not have method: {method_name}")
        
        method = getattr(subagent, method_name)
        
        if asyncio.iscoroutinefunction(method):
            return await method(**params)
        else:
            return method(**params)