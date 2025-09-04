"""Task definitions for FDJ CrewAI agents."""

from crewai import Task
from typing import Dict, Any, List


class FDJTasks:
    """Factory for creating FDJ-specific tasks."""
    
    @staticmethod
    def create_data_analysis_task(agent, game_type: str, date_range: str) -> Task:
        """Create data analysis task."""
        return Task(
            description=f"""
            Analyze {game_type} data for the period {date_range}.
            
            Your analysis should include:
            1. Statistical summary of draws/results
            2. Frequency analysis of numbers/outcomes
            3. Pattern identification (hot/cold numbers, sequences)
            4. Probability distributions
            5. Anomaly detection
            
            Provide clear insights and actionable findings.
            """,
            agent=agent,
            expected_output="Detailed statistical analysis report with key insights"
        )
    
    @staticmethod
    def create_strategy_development_task(agent, analysis_data: Dict[str, Any]) -> Task:
        """Create strategy development task."""
        return Task(
            description=f"""
            Based on the provided analysis data, develop optimal betting strategies.
            
            Consider:
            1. Risk tolerance levels (conservative, moderate, aggressive)
            2. Expected value calculations
            3. Bankroll management principles
            4. Diversification strategies
            5. Stop-loss and profit-taking rules
            
            Analysis data: {analysis_data}
            
            Provide specific, actionable strategy recommendations.
            """,
            agent=agent,
            expected_output="Comprehensive betting strategy guide with specific recommendations"
        )
    
    @staticmethod
    def create_market_research_task(agent, research_scope: str) -> Task:
        """Create market research task."""
        return Task(
            description=f"""
            Conduct market research on {research_scope}.
            
            Research areas:
            1. Player behavior trends
            2. Market sentiment analysis
            3. Seasonal patterns
            4. External factor impacts
            5. Competitive landscape
            
            Provide insights that could influence betting strategies.
            """,
            agent=agent,
            expected_output="Market research report with trend analysis and insights"
        )
    
    @staticmethod
    def create_report_generation_task(agent, data_sources: List[str]) -> Task:
        """Create comprehensive report generation task."""
        return Task(
            description=f"""
            Generate a comprehensive FDJ analysis report using data from: {', '.join(data_sources)}.
            
            Report should include:
            1. Executive summary
            2. Data analysis findings
            3. Strategy recommendations
            4. Market insights
            5. Visual charts and graphs
            6. Actionable next steps
            
            Format the report for both technical and non-technical audiences.
            """,
            agent=agent,
            expected_output="Professional analysis report with visualizations and recommendations"
        )


class TaskTemplates:
    """Pre-defined task templates for common workflows."""
    
    QUICK_ANALYSIS = {
        'name': 'Quick Game Analysis',
        'description': 'Fast analysis of recent game data',
        'estimated_time': 300
    }
    
    DEEP_DIVE = {
        'name': 'Deep Dive Analysis',
        'description': 'Comprehensive analysis with strategy development',
        'estimated_time': 1800
    }
    
    MARKET_PULSE = {
        'name': 'Market Pulse Check',
        'description': 'Current market trends and sentiment analysis',
        'estimated_time': 600
    }
    
    FULL_REPORT = {
        'name': 'Complete Analysis Report',
        'description': 'Full analysis with all agents and comprehensive reporting',
        'estimated_time': 3600
    }