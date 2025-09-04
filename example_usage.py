"""Example usage of CrewAI with multi-provider support."""

from crew_integration import MultiProviderCrewManager, AgentConfig, create_mixed_analysis_crew
import logging

# Assuming you have your existing provider_manager
# from provider_manager import ProviderManager

def example_basic_crew(provider_manager):
    """Basic example with single provider."""
    
    manager = MultiProviderCrewManager(provider_manager)
    
    # Create agent configuration
    agent_config = AgentConfig(
        role="Research Assistant",
        goal="Research topics thoroughly and provide comprehensive summaries",
        backstory="You are a diligent research assistant with access to vast knowledge.",
        provider="claude",
        model="claude-3-sonnet-20240229",
        temperature=0.5
    )
    
    # Define tasks
    tasks = [
        {
            "description": "Research the latest developments in AI safety and provide a comprehensive summary.",
            "expected_output": "A detailed summary of recent AI safety developments"
        }
    ]
    
    # Create and run crew
    crew = manager.create_crew([agent_config], tasks)
    result = crew.kickoff()
    
    print("Research Result:")
    print(result)
    return result

def example_multi_provider_crew(provider_manager):
    """Example with multiple providers for different roles."""
    
    manager = MultiProviderCrewManager(provider_manager)
    
    # Different agents with different providers
    agent_configs = [
        AgentConfig(
            role="Code Reviewer",
            goal="Review code for best practices and potential issues",
            backstory="You are a senior software engineer with expertise in code quality.",
            provider="claude",
            model="claude-3-sonnet-20240229",
            temperature=0.2  # Lower temperature for more consistent code review
        ),
        AgentConfig(
            role="Documentation Writer",
            goal="Create clear, comprehensive documentation",
            backstory="You are a technical writer specializing in developer documentation.",
            provider="openai",
            model="gpt-4",
            temperature=0.6
        ),
        AgentConfig(
            role="Test Engineer",
            goal="Design comprehensive test strategies",
            backstory="You are a QA engineer focused on thorough testing approaches.",
            provider="bedrock",
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            temperature=0.4
        )
    ]
    
    tasks = [
        {
            "description": "Review the following Python function for code quality, performance, and best practices: [code would go here]",
            "agent": 0,  # Code Reviewer
            "expected_output": "A detailed code review with specific recommendations"
        },
        {
            "description": "Create comprehensive documentation for the reviewed code including usage examples.",
            "agent": 1,  # Documentation Writer
            "expected_output": "Complete documentation with examples and API reference"
        },
        {
            "description": "Design a test strategy including unit tests, integration tests, and edge cases.",
            "agent": 2,  # Test Engineer
            "expected_output": "Comprehensive test plan with specific test cases"
        }
    ]
    
    crew = manager.create_crew(agent_configs, tasks)
    
    # Show provider information
    print("Agent Providers:", crew.get_agent_providers())
    
    result = crew.kickoff()
    return result

def example_analysis_crew(provider_manager):
    """Example using the pre-configured analysis crew."""
    
    crew = create_mixed_analysis_crew(
        provider_manager,
        analyst_provider="claude",
        writer_provider="openai"
    )
    
    # Provide input data
    inputs = {
        "data": "Sample sales data: Q1: $100k, Q2: $150k, Q3: $120k, Q4: $180k",
        "focus": "quarterly trends and growth opportunities"
    }
    
    result = crew.kickoff(inputs)
    return result

if __name__ == "__main__":
    # Example usage (you would import your actual provider_manager)
    logging.basicConfig(level=logging.INFO)
    
    # provider_manager = ProviderManager()  # Your existing provider manager
    # 
    # print("=== Basic Crew Example ===")
    # example_basic_crew(provider_manager)
    # 
    # print("\n=== Multi-Provider Crew Example ===")
    # example_multi_provider_crew(provider_manager)
    # 
    # print("\n=== Analysis Crew Example ===")
    # example_analysis_crew(provider_manager)
    
    print("Examples ready to run with your provider_manager instance")