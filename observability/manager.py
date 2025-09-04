import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from contextlib import contextmanager
from datetime import datetime
import json

@dataclass
class ObservabilityConfig:
    """Configuration for observability features."""
    enable_metrics: bool = True
    enable_tracing: bool = True
    enable_audit_integration: bool = True
    metrics_retention_hours: int = 24
    trace_sampling_rate: float = 1.0
    audit_system_endpoint: Optional[str] = None
    log_level: str = "INFO"

@dataclass
class OperationMetrics:
    """Metrics for a single operation."""
    operation_id: str
    operation_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    status: str = "running"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class ObservabilityManager:
    """Central manager for observability features."""
    
    def __init__(self, config: ObservabilityConfig):
        self.config = config
        self.logger = self._setup_logger()
        self.metrics_collector = MetricsCollector()
        self.trace_manager = TraceManager()
        self.audit_integrator = AuditIntegrator(config)
        self.logging_integrator = LoggingIntegrator(self.logger)
        
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logger for observability."""
        logger = logging.getLogger("observability")
        logger.setLevel(getattr(logging, self.config.log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    @contextmanager
    def observe_operation(self, operation_type: str, operation_id: str, **metadata):
        """Context manager for observing operations."""
        if not self.config.enable_metrics:
            yield
            return
            
        metrics = OperationMetrics(
            operation_id=operation_id,
            operation_type=operation_type,
            start_time=datetime.now(),
            metadata=metadata
        )
        
        trace_context = None
        if self.config.enable_tracing:
            trace_context = self.trace_manager.start_trace(operation_id, operation_type)
        
        try:
            self.logger.info(f"Starting operation: {operation_type} ({operation_id})")
            yield metrics
            
            metrics.status = "completed"
            self.logger.info(f"Completed operation: {operation_type} ({operation_id})")
            
        except Exception as e:
            metrics.status = "failed"
            metrics.error_message = str(e)
            self.logger.error(f"Failed operation: {operation_type} ({operation_id}): {e}")
            raise
            
        finally:
            metrics.end_time = datetime.now()
            if metrics.start_time and metrics.end_time:
                metrics.duration_ms = (
                    metrics.end_time - metrics.start_time
                ).total_seconds() * 1000
            
            self.metrics_collector.record_metrics(metrics)
            
            if trace_context:
                self.trace_manager.end_trace(trace_context, metrics.status)
            
            if self.config.enable_audit_integration:
                self.audit_integrator.send_audit_event(metrics)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        return self.metrics_collector.get_summary()
    
    def get_active_traces(self) -> List[Dict[str, Any]]:
        """Get currently active traces."""
        return self.trace_manager.get_active_traces()