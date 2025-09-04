from datetime import date, timedelta
from typing import List
from models import MetricData, WeeklyReport
from data_repository import DataRepository
from trend_analyzer import TrendAnalyzer
from outlier_detector import OutlierDetector
from report_generator import ReportGenerator

class WeeklyReportService:
    
    def __init__(self, data_repository: DataRepository):
        self.data_repository = data_repository
        self.trend_analyzer = TrendAnalyzer()
        self.outlier_detector = OutlierDetector()
        self.report_generator = ReportGenerator()
    
    def generate_weekly_report(self, week_ending: date) -> WeeklyReport:
        """Generate complete weekly report with trends and outliers."""
        if week_ending > date.today():
            raise ValueError("Cannot generate report for future dates")
        
        # Get current week data
        current_week_data = self.data_repository.get_metrics_for_week(week_ending)
        if not current_week_data:
            raise ValueError(f"No data available for week ending {week_ending}")
        
        # Get previous week data for trend analysis
        previous_week_ending = week_ending - timedelta(days=7)
        previous_week_data = self.data_repository.get_metrics_for_week(previous_week_ending)
        
        # Get historical data for outlier detection (last 4 weeks)
        historical_start = week_ending - timedelta(days=27)  # 4 weeks
        historical_data = self.data_repository.get_metrics_for_date_range(
            historical_start, week_ending
        )
        
        # Analyze trends and outliers
        trends = self.trend_analyzer.analyze_trends(current_week_data, previous_week_data)
        outliers = self.outlier_detector.detect_outliers(historical_data)
        
        # Generate report
        return self.report_generator.generate_report(week_ending, trends, outliers)
    
    def get_formatted_report(self, week_ending: date) -> str:
        """Get formatted text report."""
        report = self.generate_weekly_report(week_ending)
        return self.report_generator.format_report_text(report)