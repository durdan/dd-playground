from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    DEPLOYMENT_START = "deployment_start"
    DEPLOYMENT_SUCCESS = "deployment_success"
    DEPLOYMENT_FAILURE = "deployment_failure"
    INCIDENT_START = "incident_start"
    INCIDENT_RESOLVED = "incident_resolved"

@dataclass
class Event:
    id: str
    event_type: EventType
    timestamp: datetime
    deployment_id: Optional[str] = None
    incident_id: Optional[str] = None
    metadata: Optional[Dict] = None

class MetricsCollector:
    def __init__(self):
        self.events: List[Event] = []
    
    def record_deployment_start(self, deployment_id: str, metadata: Dict = None) -> None:
        """Record the start of a deployment"""
        if not deployment_id:
            raise ValueError("deployment_id is required")
        
        event = Event(
            id=f"deploy_start_{deployment_id}_{datetime.now().timestamp()}",
            event_type=EventType.DEPLOYMENT_START,
            timestamp=datetime.now(),
            deployment_id=deployment_id,
            metadata=metadata or {}
        )
        self.events.append(event)
    
    def record_deployment_success(self, deployment_id: str, metadata: Dict = None) -> None:
        """Record successful deployment completion"""
        if not deployment_id:
            raise ValueError("deployment_id is required")
        
        event = Event(
            id=f"deploy_success_{deployment_id}_{datetime.now().timestamp()}",
            event_type=EventType.DEPLOYMENT_SUCCESS,
            timestamp=datetime.now(),
            deployment_id=deployment_id,
            metadata=metadata or {}
        )
        self.events.append(event)
    
    def record_deployment_failure(self, deployment_id: str, metadata: Dict = None) -> None:
        """Record failed deployment"""
        if not deployment_id:
            raise ValueError("deployment_id is required")
        
        event = Event(
            id=f"deploy_failure_{deployment_id}_{datetime.now().timestamp()}",
            event_type=EventType.DEPLOYMENT_FAILURE,
            timestamp=datetime.now(),
            deployment_id=deployment_id,
            metadata=metadata or {}
        )
        self.events.append(event)
    
    def record_incident_start(self, incident_id: str, deployment_id: str = None, metadata: Dict = None) -> None:
        """Record the start of an incident"""
        if not incident_id:
            raise ValueError("incident_id is required")
        
        event = Event(
            id=f"incident_start_{incident_id}_{datetime.now().timestamp()}",
            event_type=EventType.INCIDENT_START,
            timestamp=datetime.now(),
            deployment_id=deployment_id,
            incident_id=incident_id,
            metadata=metadata or {}
        )
        self.events.append(event)
    
    def record_incident_resolved(self, incident_id: str, metadata: Dict = None) -> None:
        """Record incident resolution"""
        if not incident_id:
            raise ValueError("incident_id is required")
        
        event = Event(
            id=f"incident_resolved_{incident_id}_{datetime.now().timestamp()}",
            event_type=EventType.INCIDENT_RESOLVED,
            timestamp=datetime.now(),
            incident_id=incident_id,
            metadata=metadata or {}
        )
        self.events.append(event)
    
    def get_events(self, start_date: datetime = None, end_date: datetime = None) -> List[Event]:
        """Get events within date range"""
        filtered_events = self.events
        
        if start_date:
            filtered_events = [e for e in filtered_events if e.timestamp >= start_date]
        
        if end_date:
            filtered_events = [e for e in filtered_events if e.timestamp <= end_date]
        
        return filtered_events