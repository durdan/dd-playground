import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TraceContext:
    """Context for a distributed trace."""
    trace_id: str
    operation_id: str
    operation_type: str
    start_time: datetime
    parent_trace_id: Optional[str] = None
    spans: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.spans is None:
            self.spans = []

class TraceManager:
    """Manages distributed tracing for operations."""
    
    def __init__(self):
        self.active_traces: Dict[str, TraceContext] = {}
        self.completed_traces: List[TraceContext] = []
    
    def start_trace(self, operation_id: str, operation_type: str, 
                   parent_trace_id: Optional[str] = None) -> TraceContext:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())
        
        trace_context = TraceContext(
            trace_id=trace_id,
            operation_id=operation_id,
            operation_type=operation_type,
            start_time=datetime.now(),
            parent_trace_id=parent_trace_id
        )
        
        self.active_traces[trace_id] = trace_context
        return trace_context
    
    def add_span(self, trace_id: str, span_name: str, **span_data):
        """Add a span to an existing trace."""
        if trace_id in self.active_traces:
            span = {
                "name": span_name,
                "timestamp": datetime.now(),
                "data": span_data
            }
            self.active_traces[trace_id].spans.append(span)
    
    def end_trace(self, trace_context: TraceContext, status: str):
        """End a trace and move it to completed traces."""
        trace_id = trace_context.trace_id
        
        if trace_id in self.active_traces:
            trace_context.spans.append({
                "name": "operation_completed",
                "timestamp": datetime.now(),
                "data": {"status": status}
            })
            
            self.completed_traces.append(trace_context)
            del self.active_traces[trace_id]
    
    def get_active_traces(self) -> List[Dict[str, Any]]:
        """Get information about active traces."""
        return [
            {
                "trace_id": trace.trace_id,
                "operation_id": trace.operation_id,
                "operation_type": trace.operation_type,
                "start_time": trace.start_time.isoformat(),
                "span_count": len(trace.spans)
            }
            for trace in self.active_traces.values()
        ]
    
    def get_trace_details(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific trace."""
        trace = self.active_traces.get(trace_id)
        if not trace:
            # Check completed traces
            for completed_trace in self.completed_traces:
                if completed_trace.trace_id == trace_id:
                    trace = completed_trace
                    break
        
        if trace:
            return {
                "trace_id": trace.trace_id,
                "operation_id": trace.operation_id,
                "operation_type": trace.operation_type,
                "start_time": trace.start_time.isoformat(),
                "parent_trace_id": trace.parent_trace_id,
                "spans": trace.spans
            }
        
        return None