from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class TestRequest:
    code_path: str
    test_types: List[TestType]
    coverage_threshold: float = 0.8
    priority: int = 1
    metadata: Dict[str, Any] = None

@dataclass
class TestResult:
    agent_name: str
    test_type: TestType
    test_code: str
    coverage_info: Dict[str, float]
    execution_time: float
    success: bool
    errors: List[str] = None

class TestCoordinator:
    def __init__(self, subagent_manager, crewai_manager, config_manager):
        self.subagent_manager = subagent_manager
        self.crewai_manager = crewai_manager
        self.config_manager = config_manager
        self.test_aggregator = TestAggregator()
        self.logger = logging.getLogger(__name__)

    async def generate_comprehensive_tests(self, request: TestRequest) -> Dict[str, List[TestResult]]:
        """Coordinate test generation across all available agents."""
        if not request.code_path:
            raise ValueError("Code path is required")
        
        strategy = self._create_test_strategy(request)
        
        # Run agents in parallel based on strategy
        tasks = []
        
        if strategy.use_subagents:
            tasks.append(self._run_subagents(request, strategy.subagent_types))
        
        if strategy.use_crewai:
            tasks.append(self._run_crewai_agents(request, strategy.crewai_types))
        
        if not tasks:
            raise ValueError("No agents configured for the requested test types")
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate and deduplicate results
        all_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Agent execution failed: {result}")
                continue
            all_results.extend(result)
        
        return self.test_aggregator.aggregate_results(all_results)

    def _create_test_strategy(self, request: TestRequest) -> 'TestStrategy':
        """Determine which agents should handle which test types."""
        config = self.config_manager.get_strategy_config()
        
        subagent_types = []
        crewai_types = []
        
        for test_type in request.test_types:
            if test_type in config.get('subagent_specialties', []):
                subagent_types.append(test_type)
            if test_type in config.get('crewai_specialties', []):
                crewai_types.append(test_type)
        
        return TestStrategy(
            use_subagents=bool(subagent_types),
            use_crewai=bool(crewai_types),
            subagent_types=subagent_types,
            crewai_types=crewai_types
        )

    async def _run_subagents(self, request: TestRequest, test_types: List[TestType]) -> List[TestResult]:
        """Execute existing subagent test generators."""
        return await self.subagent_manager.generate_tests(request, test_types)

    async def _run_crewai_agents(self, request: TestRequest, test_types: List[TestType]) -> List[TestResult]:
        """Execute CrewAI test writer agents."""
        return await self.crewai_manager.generate_tests(request, test_types)

@dataclass
class TestStrategy:
    use_subagents: bool
    use_crewai: bool
    subagent_types: List[TestType]
    crewai_types: List[TestType]