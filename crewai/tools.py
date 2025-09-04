"""Tools integration for FDJ CrewAI agents."""

from crewai_tools import BaseTool
from typing import Any, Dict, Optional
import sys
import os

# Add parent directory to path to import existing FDJ modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fdj.data_fetcher import DataFetcher
    from fdj.analyzer import Analyzer
    from fdj.visualizer import Visualizer
except ImportError:
    # Fallback if modules don't exist yet
    DataFetcher = None
    Analyzer = None
    Visualizer = None


class FDJDataFetcherTool(BaseTool):
    """Tool for fetching FDJ game data."""
    
    name: str = "FDJ Data Fetcher"
    description: str = "Fetch historical and current FDJ game data"
    
    def _run(self, game_type: str, date_range: str = "30d") -> str:
        """Fetch FDJ data for specified game and date range."""
        if DataFetcher is None:
            return "DataFetcher module not available"
        
        try:
            fetcher = DataFetcher()
            data = fetcher.fetch_game_data(game_type, date_range)
            return f"Successfully fetched {len(data)} records for {game_type}"
        except Exception as e:
            return f"Error fetching data: {str(e)}"


class FDJAnalyzerTool(BaseTool):
    """Tool for analyzing FDJ game data."""
    
    name: str = "FDJ Analyzer"
    description: str = "Analyze FDJ game data for patterns and statistics"
    
    def _run(self, data: Any, analysis_type: str = "full") -> str:
        """Analyze FDJ data."""
        if Analyzer is None:
            return "Analyzer module not available"
        
        try:
            analyzer = Analyzer()
            results = analyzer.analyze(data, analysis_type)
            return f"Analysis completed: {results.get('summary', 'No summary available')}"
        except Exception as e:
            return f"Error analyzing data: {str(e)}"


class FDJVisualizerTool(BaseTool):
    """Tool for creating visualizations of FDJ data."""
    
    name: str = "FDJ Visualizer"
    description: str = "Create charts and visualizations for FDJ analysis"
    
    def _run(self, data: Any, chart_type: str = "frequency") -> str:
        """Create visualizations."""
        if Visualizer is None:
            return "Visualizer module not available"
        
        try:
            visualizer = Visualizer()
            chart_path = visualizer.create_chart(data, chart_type)
            return f"Chart created: {chart_path}"
        except Exception as e:
            return f"Error creating visualization: {str(e)}"


class FDJTools:
    """Factory for creating FDJ tools."""
    
    @staticmethod
    def create_tool_set() -> Dict[str, BaseTool]:
        """Create complete set of FDJ tools."""
        return {
            'data_fetcher': FDJDataFetcherTool(),
            'analyzer': FDJAnalyzerTool(),
            'visualizer': FDJVisualizerTool(),
            'statistics_calculator': FDJAnalyzerTool(),
            'pattern_analyzer': FDJAnalyzerTool(),
            'probability_calculator': FDJAnalyzerTool(),
            'risk_analyzer': FDJAnalyzerTool(),
            'strategy_optimizer': FDJAnalyzerTool(),
            'market_data_fetcher': FDJDataFetcherTool(),
            'trend_analyzer': FDJAnalyzerTool(),
            'behavior_analyzer': FDJAnalyzerTool(),
            'report_builder': FDJVisualizerTool(),
            'chart_generator': FDJVisualizerTool(),
            'export_manager': FDJVisualizerTool()
        }