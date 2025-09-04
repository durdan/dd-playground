import pytest
from agents.base_agent import BaseAgent, ResearchAgent, WriterAgent


class TestBaseAgent:
    
    def test_base_agent_creation(self):
        """Test BaseAgent initialization."""
        agent = BaseAgent(
            role="Test Role",
            goal="Test Goal", 
            backstory="Test Backstory"
        )
        
        assert agent.role == "Test Role"
        assert agent.goal == "Test Goal"
        assert agent.backstory == "Test Backstory"
    
    def test_create_agent(self):
        """Test agent creation."""
        base_agent = BaseAgent(
            role="Test Role",
            goal="Test Goal",
            backstory="Test Backstory"
        )
        
        crew_agent = base_agent.create_agent()
        assert crew_agent.role == "Test Role"
        assert crew_agent.goal == "Test Goal"


class TestSpecializedAgents:
    
    def test_research_agent(self):
        """Test ResearchAgent initialization."""
        agent = ResearchAgent()
        assert agent.role == "Research Specialist"
        assert "research" in agent.goal.lower()
    
    def test_writer_agent(self):
        """Test WriterAgent initialization."""
        agent = WriterAgent()
        assert agent.role == "Content Writer"
        assert "content" in agent.goal.lower()