"""CrewAI crew for coordinating AI providers"""
from crewai import Agent, Task, Crew, Process
from crew_tools import ProviderManagerTool, LoadBalancerTool
from typing import List, Dict, Any

class AIProviderCrew:
    def __init__(self):
        self.provider_tool = ProviderManagerTool()
        self.load_balancer_tool = LoadBalancerTool()
        self._setup_agents()
        self._setup_crew()
    
    def _setup_agents(self):
        """Initialize specialized agents"""
        self.coordinator_agent = Agent(
            role='AI Provider Coordinator',
            goal='Efficiently route requests to the best available AI provider',
            backstory='''You are an expert at managing multiple AI providers and 
                        ensuring optimal performance and cost efficiency.''',
            tools=[self.provider_tool, self.load_balancer_tool],
            verbose=True
        )
        
        self.monitor_agent = Agent(
            role='Performance Monitor',
            goal='Track and analyze provider performance metrics',
            backstory='''You specialize in monitoring AI provider performance, 
                        identifying bottlenecks, and suggesting optimizations.''',
            tools=[self.provider_tool],
            verbose=True
        )
        
        self.quality_agent = Agent(
            role='Response Quality Assessor',
            goal='Evaluate and ensure high-quality responses from providers',
            backstory='''You are responsible for maintaining response quality 
                        standards across all AI providers.''',
            tools=[self.provider_tool],
            verbose=True
        )
    
    def _setup_crew(self):
        """Setup the crew with agents and process"""
        self.crew = Crew(
            agents=[self.coordinator_agent, self.monitor_agent, self.quality_agent],
            process=Process.sequential,
            verbose=True
        )
    
    def process_request(self, prompt: str, requirements: Dict[str, Any] = None) -> str:
        """Process a request through the crew"""
        requirements = requirements or {}
        
        # Create tasks for the crew
        coordination_task = Task(
            description=f'''Route this request to the best provider: "{prompt}"
                           Requirements: {requirements}
                           Use the provider manager tool to find the optimal provider.''',
            agent=self.coordinator_agent,
            expected_output="Provider selection and response generation"
        )
        
        monitoring_task = Task(
            description='''Monitor the performance of the selected provider and 
                          provide metrics analysis.''',
            agent=self.monitor_agent,
            expected_output="Performance metrics and analysis"
        )
        
        quality_task = Task(
            description='''Assess the quality of the generated response and 
                          provide feedback.''',
            agent=self.quality_agent,
            expected_output="Quality assessment and recommendations"
        )
        
        # Execute tasks
        self.crew.tasks = [coordination_task, monitoring_task, quality_task]
        result = self.crew.kickoff()
        
        return str(result)
    
    def get_provider_status(self) -> str:
        """Get current status of all providers"""
        status_task = Task(
            description='Get comprehensive status of all AI providers including metrics.',
            agent=self.monitor_agent,
            expected_output="Complete provider status report"
        )
        
        self.crew.tasks = [status_task]
        result = self.crew.kickoff()
        return str(result)
    
    def optimize_routing(self) -> str:
        """Optimize provider routing based on current performance"""
        optimization_task = Task(
            description='''Analyze current provider performance and suggest 
                          routing optimizations for better efficiency.''',
            agent=self.coordinator_agent,
            expected_output="Routing optimization recommendations"
        )
        
        self.crew.tasks = [optimization_task]
        result = self.crew.kickoff()
        return str(result)