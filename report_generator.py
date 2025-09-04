from typing import List
from models import WeeklyReport, TrendResult, OutlierResult
from datetime import date

class ReportGenerator:
    
    def generate_report(self, week_ending: date, trends: List[TrendResult], 
                       outliers: List[OutlierResult]) -> WeeklyReport:
        """Generate a formatted weekly report."""
        summary = self._create_summary(trends, outliers)
        
        return WeeklyReport(
            week_ending=week_ending,
            trends=trends,
            outliers=outliers,
            summary=summary
        )
    
    def format_report_text(self, report: WeeklyReport) -> str:
        """Format report as readable text."""
        lines = [
            f"WEEKLY REPORT - Week Ending {report.week_ending}",
            "=" * 50,
            "",
            "EXECUTIVE SUMMARY:",
            report.summary,
            "",
            "TREND ANALYSIS:",
        ]
        
        for trend in report.trends:
            direction_symbol = self._get_trend_symbol(trend.trend_direction)
            if trend.change_percent is not None:
                lines.append(
                    f"  {direction_symbol} {trend.metric_name}: "
                    f"{trend.current_value:.2f} ({trend.change_percent:+.1f}%)"
                )
            else:
                lines.append(f"  📊 {trend.metric_name}: {trend.current_value:.2f} (new metric)")
        
        if report.outliers:
            lines.extend(["", "OUTLIERS DETECTED:"])
            for outlier in report.outliers:
                lines.append(
                    f"  ⚠️  {outlier.metric_name}: {len(outlier.outlier_values)} outlier(s) "
                    f"detected on {', '.join(str(d) for d in outlier.outlier_dates)}"
                )
        
        return "\n".join(lines)
    
    def _create_summary(self, trends: List[TrendResult], outliers: List[OutlierResult]) -> str:
        """Create executive summary."""
        total_metrics = len(trends)
        up_trends = len([t for t in trends if t.trend_direction == 'up'])
        down_trends = len([t for t in trends if t.trend_direction == 'down'])
        outlier_count = sum(len(o.outlier_values) for o in outliers)
        
        summary_parts = [
            f"Analyzed {total_metrics} metrics this week.",
            f"{up_trends} metrics trending up, {down_trends} trending down."
        ]
        
        if outlier_count > 0:
            summary_parts.append(f"{outlier_count} outliers detected requiring attention.")
        else:
            summary_parts.append("No significant outliers detected.")
        
        return " ".join(summary_parts)
    
    def _get_trend_symbol(self, direction: str) -> str:
        """Get emoji symbol for trend direction."""
        symbols = {
            'up': '📈',
            'down': '📉',
            'stable': '➡️',
            'new': '📊'
        }
        return symbols.get(direction, '❓')