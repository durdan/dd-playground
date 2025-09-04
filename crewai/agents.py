"""FDJ specialized agents for CrewAI."""

from crewai import Agent
from typing import Dict, Any
import os


class FDJAgents:
    """Factory for creating FDJ-specific agents."""
    
    def __init__(self, tools: Dict[str, Any]):
        self.tools = tools
    
    def create_data_analyst(self) -> Agent:
        """Create data analysis agent for FDJ games."""
        return Agent(
            role='FDJ Data Analyst',
            goal='Analyze FDJ game data to identify patterns and trends',
            backstory="""You are an expert data analyst specializing in French lottery 
            and betting games. You excel at finding statistical patterns, calculating 
            probabilities, and providing data-driven insights for FDJ games.""",
            tools=[
                self.tools.get('data_fetcher'),
                self.tools.get('statistics_calculator'),
                self.tools.get('pattern_analyzer')
            ],
            verbose=True,
            allow_delegation=False
        )
    
    def create_strategy_advisor(self) -> Agent:
        """Create betting strategy advisor agent."""
        return Agent(
            role='FDJ Strategy Advisor',
            goal='Develop and recommend optimal betting strategies',
            backstory="""You are a strategic advisor with deep knowledge of probability 
            theory and risk management. You specialize in creating balanced betting 
            strategies that maximize expected value while managing risk.""",
            tools=[
                self.tools.get('probability_calculator'),
                self.tools.get('risk_analyzer'),
                self.tools.get('strategy_optimizer')
            ],
            verbose=True,
            allow_delegation=False
        )
    
    def create_market_researcher(self) -> Agent:
        """Create market research agent for FDJ trends."""
        return Agent(
            role='FDJ Market Researcher',
            goal='Research market trends and player behavior patterns',
            backstory="""You are a market research specialist focused on gambling 
            and lottery markets. You analyze player behavior, market trends, and 
            external factors that influence FDJ game outcomes.""",
            tools=[
                self.tools.get('market_data_fetcher'),
                self.tools.get('trend_analyzer'),
                self.tools.get('behavior_analyzer')
            ],
            verbose=True,
            allow_delegation=False
        )
    
    def create_report_generator(self) -> Agent:
        """Create report generation agent."""
        return Agent(
            role='FDJ Report Generator',
            goal='Generate comprehensive reports and visualizations',
            backstory="""You are a technical writer and data visualization expert. 
            You excel at creating clear, actionable reports that summarize complex 
            analysis and present insights in an accessible format.""",
            tools=[
                self.tools.get('report_builder'),
                self.tools.get('chart_generator'),
                self.tools.get('export_manager')
            ],
            verbose=True,
            allow_delegation=False
        )


def create_agent_config() -> Dict[str, Dict[str, Any]]:
    """Create default agent configurations."""
    return {
        'data_analyst': {
            'max_iter': 10,
            'max_execution_time': 300,
            'memory': True
        },
        'strategy_advisor': {
            'max_iter': 15,
            'max_execution_time': 600,
            'memory': True
        },
        'market_researcher': {
            'max_iter': 12,
            'max_execution_time': 400,
            'memory': True
        },
        'report_generator': {
            'max_iter': 8,
            'max_execution_time': 200,
            'memory': True
        }
    }