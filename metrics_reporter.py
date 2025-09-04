from datetime import datetime
from .metrics_calculator import MetricsSummary, MetricsCalculator

class MetricsReporter:
    def __init__(self, calculator: MetricsCalculator):
        self.calculator = calculator
    
    def generate_report(self, start_date: datetime = None, end_date: datetime = None) -> str:
        """Generate a formatted metrics report"""
        metrics = self.calculator.calculate_metrics(start_date, end_date)
        
        period_str = self._format_period(start_date, end_date)
        
        report = f"""
=== DEPLOYMENT & OPERATIONAL METRICS REPORT ===
Period: {period_str}

DEPLOYMENT METRICS:
  Total Deployments: {metrics.total_deployments}
  Successful: {metrics.successful_deployments}
  Failed: {metrics.failed_deployments}
  Success Rate: {metrics.success_rate:.1f}%
  Failure Rate: {metrics.failure_rate:.1f}%

DORA METRICS:
  Change Failure Rate (CFR): {metrics.change_failure_rate:.1f}%
  Mean Lead Time: {metrics.mean_lead_time_hours:.2f} hours
  Mean Time To Recovery (MTTR): {metrics.mean_time_to_recovery_hours:.2f} hours

INCIDENT METRICS:
  Total Incidents: {metrics.total_incidents}
  Resolved Incidents: {metrics.resolved_incidents}
  Open Incidents: {metrics.total_incidents - metrics.resolved_incidents}

=== END REPORT ===
        """.strip()
        
        return report
    
    def _format_period(self, start_date: datetime, end_date: datetime) -> str:
        """Format the reporting period"""
        if not start_date and not end_date:
            return "All Time"
        elif start_date and not end_date:
            return f"From {start_date.strftime('%Y-%m-%d %H:%M')}"
        elif not start_date and end_date:
            return f"Until {end_date.strftime('%Y-%m-%d %H:%M')}"
        else:
            return f"{start_date.strftime('%Y-%m-%d %H:%M')} to {end_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_metrics_json(self, start_date: datetime = None, end_date: datetime = None) -> dict:
        """Get metrics as JSON-serializable dictionary"""
        metrics = self.calculator.calculate_metrics(start_date, end_date)
        
        return {
            'period': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            },
            'deployment_metrics': {
                'total_deployments': metrics.total_deployments,
                'successful_deployments': metrics.successful_deployments,
                'failed_deployments': metrics.failed_deployments,
                'success_rate': round(metrics.success_rate, 2),
                'failure_rate': round(metrics.failure_rate, 2)
            },
            'dora_metrics': {
                'change_failure_rate': round(metrics.change_failure_rate, 2),
                'mean_lead_time_hours': round(metrics.mean_lead_time_hours, 2),
                'mean_time_to_recovery_hours': round(metrics.mean_time_to_recovery_hours, 2)
            },
            'incident_metrics': {
                'total_incidents': metrics.total_incidents,
                'resolved_incidents': metrics.resolved_incidents,
                'open_incidents': metrics.total_incidents - metrics.resolved_incidents
            }
        }