from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from .metrics_collector import Event, EventType, MetricsCollector

@dataclass
class MetricsSummary:
    total_deployments: int
    successful_deployments: int
    failed_deployments: int
    success_rate: float
    failure_rate: float
    change_failure_rate: float
    mean_lead_time_hours: float
    mean_time_to_recovery_hours: float
    total_incidents: int
    resolved_incidents: int

class MetricsCalculator:
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def calculate_metrics(self, start_date: datetime = None, end_date: datetime = None) -> MetricsSummary:
        """Calculate comprehensive metrics for the given time period"""
        events = self.collector.get_events(start_date, end_date)
        
        deployment_stats = self._calculate_deployment_stats(events)
        lead_time = self._calculate_mean_lead_time(events)
        cfr = self._calculate_change_failure_rate(events)
        mttr = self._calculate_mean_time_to_recovery(events)
        incident_stats = self._calculate_incident_stats(events)
        
        return MetricsSummary(
            total_deployments=deployment_stats['total'],
            successful_deployments=deployment_stats['successful'],
            failed_deployments=deployment_stats['failed'],
            success_rate=deployment_stats['success_rate'],
            failure_rate=deployment_stats['failure_rate'],
            change_failure_rate=cfr,
            mean_lead_time_hours=lead_time,
            mean_time_to_recovery_hours=mttr,
            total_incidents=incident_stats['total'],
            resolved_incidents=incident_stats['resolved']
        )
    
    def _calculate_deployment_stats(self, events: List[Event]) -> Dict:
        """Calculate deployment success/failure statistics"""
        deployment_outcomes = defaultdict(list)
        
        for event in events:
            if event.event_type in [EventType.DEPLOYMENT_SUCCESS, EventType.DEPLOYMENT_FAILURE]:
                deployment_outcomes[event.deployment_id].append(event.event_type)
        
        total = len(deployment_outcomes)
        successful = sum(1 for outcomes in deployment_outcomes.values() 
                        if EventType.DEPLOYMENT_SUCCESS in outcomes)
        failed = sum(1 for outcomes in deployment_outcomes.values() 
                    if EventType.DEPLOYMENT_FAILURE in outcomes)
        
        success_rate = (successful / total * 100) if total > 0 else 0
        failure_rate = (failed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate,
            'failure_rate': failure_rate
        }
    
    def _calculate_mean_lead_time(self, events: List[Event]) -> float:
        """Calculate mean lead time from deployment start to completion"""
        deployment_times = defaultdict(dict)
        
        for event in events:
            if event.deployment_id and event.event_type == EventType.DEPLOYMENT_START:
                deployment_times[event.deployment_id]['start'] = event.timestamp
            elif event.deployment_id and event.event_type in [EventType.DEPLOYMENT_SUCCESS, EventType.DEPLOYMENT_FAILURE]:
                deployment_times[event.deployment_id]['end'] = event.timestamp
        
        lead_times = []
        for deployment_id, times in deployment_times.items():
            if 'start' in times and 'end' in times:
                lead_time = (times['end'] - times['start']).total_seconds() / 3600  # Convert to hours
                lead_times.append(lead_time)
        
        return sum(lead_times) / len(lead_times) if lead_times else 0
    
    def _calculate_change_failure_rate(self, events: List[Event]) -> float:
        """Calculate Change Failure Rate - % of deployments that cause incidents"""
        deployments_with_incidents = set()
        all_deployments = set()
        
        for event in events:
            if event.deployment_id:
                all_deployments.add(event.deployment_id)
                
                if event.event_type == EventType.INCIDENT_START:
                    deployments_with_incidents.add(event.deployment_id)
        
        total_deployments = len(all_deployments)
        failed_deployments = len(deployments_with_incidents)
        
        return (failed_deployments / total_deployments * 100) if total_deployments > 0 else 0
    
    def _calculate_mean_time_to_recovery(self, events: List[Event]) -> float:
        """Calculate Mean Time To Recovery for incidents"""
        incident_times = defaultdict(dict)
        
        for event in events:
            if event.incident_id and event.event_type == EventType.INCIDENT_START:
                incident_times[event.incident_id]['start'] = event.timestamp
            elif event.incident_id and event.event_type == EventType.INCIDENT_RESOLVED:
                incident_times[event.incident_id]['end'] = event.timestamp
        
        recovery_times = []
        for incident_id, times in incident_times.items():
            if 'start' in times and 'end' in times:
                recovery_time = (times['end'] - times['start']).total_seconds() / 3600  # Convert to hours
                recovery_times.append(recovery_time)
        
        return sum(recovery_times) / len(recovery_times) if recovery_times else 0
    
    def _calculate_incident_stats(self, events: List[Event]) -> Dict:
        """Calculate incident statistics"""
        incidents_started = set()
        incidents_resolved = set()
        
        for event in events:
            if event.event_type == EventType.INCIDENT_START:
                incidents_started.add(event.incident_id)
            elif event.event_type == EventType.INCIDENT_RESOLVED:
                incidents_resolved.add(event.incident_id)
        
        return {
            'total': len(incidents_started),
            'resolved': len(incidents_resolved)
        }