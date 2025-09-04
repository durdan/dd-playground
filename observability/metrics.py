import time
from typing import Dict, Any, List
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading

class MetricsCollector:
    """Collects and aggregates CrewAI operation metrics"""
    
    def __init__(self, config):
        self.config = config
        self._lock = threading.Lock()
        self._executions = {}  # execution_id -> execution_data
        self._metrics_history = deque(maxlen=10000)  # Recent metrics
        self._aggregated_metrics = defaultdict(lambda: defaultdict(int))
    
    def start_execution_metrics(self, execution_id: str, crew_id: str):
        """Start collecting metrics for an execution"""
        with self._lock:
            self._executions[execution_id] = {
                "crew_id": crew_id,
                "start_time": time.time(),
                "start_datetime": datetime.now(),
                "agents_count": 0,
                "tasks_count": 0,
                "errors": []
            }
    
    def end_execution_metrics(self, execution_id: str, success: bool):
        """End metrics collection for an execution"""
        with self._lock:
            if execution_id not in self._executions:
                return
            
            execution_data = self._executions[execution_id]
            end_time = time.time()
            duration = end_time - execution_data["start_time"]
            
            # Create metrics record
            metrics_record = {
                "execution_id": execution_id,
                "crew_id": execution_data["crew_id"],
                "duration_seconds": duration,
                "success": success,
                "timestamp": datetime.now(),
                "agents_count": execution_data["agents_count"],
                "tasks_count": execution_data["tasks_count"],
                "error_count": len(execution_data["errors"])
            }
            
            self._metrics_history.append(metrics_record)
            
            # Update aggregated metrics
            crew_id = execution_data["crew_id"]
            self._aggregated_metrics[crew_id]["total_executions"] += 1
            self._aggregated_metrics[crew_id]["total_duration"] += duration
            
            if success:
                self._aggregated_metrics[crew_id]["successful_executions"] += 1
            else:
                self._aggregated_metrics[crew_id]["failed_executions"] += 1
            
            # Clean up
            del self._executions[execution_id]
    
    def record_agent_activity(self, execution_id: str, agent_id: str, activity: str):
        """Record agent activity metrics"""
        with self._lock:
            if execution_id in self._executions:
                self._executions[execution_id]["agents_count"] += 1
    
    def record_task_completion(self, execution_id: str, task_id: str, duration: float):
        """Record task completion metrics"""
        with self._lock:
            if execution_id in self._executions:
                self._executions[execution_id]["tasks_count"] += 1
    
    def record_error(self, execution_id: str, error: str):
        """Record error metrics"""
        with self._lock:
            if execution_id in self._executions:
                self._executions[execution_id]["errors"].append({
                    "error": error,
                    "timestamp": datetime.now()
                })
    
    def get_summary(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for time range"""
        cutoff_time = datetime.now() - timedelta(hours=time_range_hours)
        
        with self._lock:
            recent_metrics = [
                m for m in self._metrics_history 
                if m["timestamp"] >= cutoff_time
            ]
            
            if not recent_metrics:
                return {"message": "no_metrics_in_range", "time_range_hours": time_range_hours}
            
            total_executions = len(recent_metrics)
            successful_executions = sum(1 for m in recent_metrics if m["success"])
            failed_executions = total_executions - successful_executions
            
            avg_duration = sum(m["duration_seconds"] for m in recent_metrics) / total_executions
            
            return {
                "time_range_hours": time_range_hours,
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
                "average_duration_seconds": avg_duration,
                "crew_breakdown": self._get_crew_breakdown(recent_metrics)
            }
    
    def _get_crew_breakdown(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get per-crew metrics breakdown"""
        crew_stats = defaultdict(lambda: {"executions": 0, "successes": 0, "total_duration": 0})
        
        for metric in metrics:
            crew_id = metric["crew_id"]
            crew_stats[crew_id]["executions"] += 1
            crew_stats[crew_id]["total_duration"] += metric["duration_seconds"]
            if metric["success"]:
                crew_stats[crew_id]["successes"] += 1
        
        return dict(crew_stats)