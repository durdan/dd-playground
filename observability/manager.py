import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ObservabilityConfig:
    """Configuration for observability system"""
    metrics_enabled: bool = True
    tracing_enabled: bool = True
    audit_integration_enabled: bool = True
    health_monitoring_enabled: bool = True
    log_level: str = "INFO"
    metrics_retention_days: int = 30
    trace_sampling_rate: float = 1.0

class ObservabilityManager:
    """Central manager for CrewAI observability"""
    
    def __init__(self, config: ObservabilityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Initialize components
        self.metrics_collector = MetricsCollector(config)
        self.tracing_service = TracingService(config)
        self.audit_integrator = AuditIntegrator(config)
        self.logging_enhancer = LoggingEnhancer(config)
        self.health_monitor = HealthMonitor(config)
        
        self.logger.info("ObservabilityManager initialized")
    
    def _setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def start_crew_execution(self, crew_id: str, crew_config: Dict[str, Any]) -> str:
        """Start observability tracking for crew execution"""
        if not crew_id:
            raise ValueError("crew_id cannot be empty")
        
        execution_id = f"exec_{crew_id}_{int(time.time())}"
        
        # Start tracing
        if self.config.tracing_enabled:
            self.tracing_service.start_trace(execution_id, crew_id, crew_config)
        
        # Initialize metrics
        if self.config.metrics_enabled:
            self.metrics_collector.start_execution_metrics(execution_id, crew_id)
        
        # Create audit entry
        if self.config.audit_integration_enabled:
            self.audit_integrator.log_execution_start(execution_id, crew_id, crew_config)
        
        # Enhanced logging
        self.logging_enhancer.log_with_context(
            "INFO", f"Started crew execution: {crew_id}", 
            {"execution_id": execution_id, "crew_id": crew_id}
        )
        
        return execution_id
    
    def end_crew_execution(self, execution_id: str, success: bool, result: Optional[Dict[str, Any]] = None):
        """End observability tracking for crew execution"""
        if not execution_id:
            raise ValueError("execution_id cannot be empty")
        
        # End tracing
        if self.config.tracing_enabled:
            self.tracing_service.end_trace(execution_id, success, result)
        
        # Finalize metrics
        if self.config.metrics_enabled:
            self.metrics_collector.end_execution_metrics(execution_id, success)
        
        # Create audit entry
        if self.config.audit_integration_enabled:
            self.audit_integrator.log_execution_end(execution_id, success, result)
        
        # Enhanced logging
        status = "SUCCESS" if success else "FAILURE"
        self.logging_enhancer.log_with_context(
            "INFO", f"Ended crew execution: {status}", 
            {"execution_id": execution_id, "success": success}
        )
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current system health status"""
        if not self.config.health_monitoring_enabled:
            return {"status": "monitoring_disabled"}
        
        return self.health_monitor.get_status()
    
    def get_metrics_summary(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for specified time range"""
        if not self.config.metrics_enabled:
            return {"error": "metrics_disabled"}
        
        return self.metrics_collector.get_summary(time_range_hours)