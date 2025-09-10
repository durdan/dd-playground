import asyncio
import time
import psutil
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque
import statistics

@dataclass
class PerformanceMetric:
    name: str
    value: float
    timestamp: float
    category: str
    threshold: Optional[float] = None

@dataclass
class Bottleneck:
    component: str
    metric: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    suggested_fix: str
    impact_score: float

class PerformanceOptimizer:
    """Main optimizer subagent that identifies bottlenecks and implements improvements."""
    
    def __init__(self, monitoring_window: int = 300):  # 5 minutes
        self.monitoring_window = monitoring_window
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.bottlenecks: List[Bottleneck] = []
        self.optimizations_applied: List[str] = []
        self.logger = logging.getLogger(__name__)
        
        # Performance thresholds
        self.thresholds = {
            'response_time': 2.0,  # seconds
            'memory_usage': 80.0,  # percentage
            'cpu_usage': 70.0,     # percentage
            'cache_hit_rate': 80.0, # percentage
            'api_error_rate': 5.0,  # percentage
        }
    
    async def analyze_performance(self) -> List[Bottleneck]:
        """Analyze current performance and identify bottlenecks."""
        bottlenecks = []
        
        # Analyze response times
        response_times = self._get_recent_metrics('response_time')
        if response_times:
            avg_response_time = statistics.mean(response_times)
            if avg_response_time > self.thresholds['response_time']:
                bottlenecks.append(Bottleneck(
                    component='chat_system',
                    metric='response_time',
                    severity='high' if avg_response_time > 5.0 else 'medium',
                    description=f'Average response time: {avg_response_time:.2f}s',
                    suggested_fix='Enable response streaming, optimize AI API calls',
                    impact_score=avg_response_time / self.thresholds['response_time']
                ))
        
        # Analyze memory usage
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > self.thresholds['memory_usage']:
            bottlenecks.append(Bottleneck(
                component='system',
                metric='memory_usage',
                severity='critical' if memory_percent > 90 else 'high',
                description=f'Memory usage: {memory_percent:.1f}%',
                suggested_fix='Implement aggressive caching cleanup, lazy loading',
                impact_score=memory_percent / self.thresholds['memory_usage']
            ))
        
        # Analyze cache performance
        cache_hit_rates = self._get_recent_metrics('cache_hit_rate')
        if cache_hit_rates:
            avg_hit_rate = statistics.mean(cache_hit_rates)
            if avg_hit_rate < self.thresholds['cache_hit_rate']:
                bottlenecks.append(Bottleneck(
                    component='cache_manager',
                    metric='cache_hit_rate',
                    severity='medium',
                    description=f'Cache hit rate: {avg_hit_rate:.1f}%',
                    suggested_fix='Optimize cache keys, increase cache size, improve eviction policy',
                    impact_score=(self.thresholds['cache_hit_rate'] - avg_hit_rate) / self.thresholds['cache_hit_rate']
                ))
        
        # Analyze API error rates
        api_error_rates = self._get_recent_metrics('api_error_rate')
        if api_error_rates:
            avg_error_rate = statistics.mean(api_error_rates)
            if avg_error_rate > self.thresholds['api_error_rate']:
                bottlenecks.append(Bottleneck(
                    component='ai_api',
                    metric='error_rate',
                    severity='high' if avg_error_rate > 10 else 'medium',
                    description=f'API error rate: {avg_error_rate:.1f}%',
                    suggested_fix='Implement retry logic, circuit breaker, fallback responses',
                    impact_score=avg_error_rate / self.thresholds['api_error_rate']
                ))
        
        self.bottlenecks = sorted(bottlenecks, key=lambda x: x.impact_score, reverse=True)
        return self.bottlenecks
    
    def _get_recent_metrics(self, metric_name: str) -> List[float]:
        """Get recent metrics within the monitoring window."""
        current_time = time.time()
        cutoff_time = current_time - self.monitoring_window
        
        recent_metrics = []
        for metric in self.metrics_history[metric_name]:
            if metric.timestamp >= cutoff_time:
                recent_metrics.append(metric.value)
        
        return recent_metrics
    
    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        self.metrics_history[metric.name].append(metric)
    
    async def suggest_optimizations(self) -> List[str]:
        """Suggest optimizations based on current bottlenecks."""
        suggestions = []
        
        for bottleneck in self.bottlenecks:
            if bottleneck.severity in ['high', 'critical']:
                suggestions.append(f"{bottleneck.component}: {bottleneck.suggested_fix}")
        
        return suggestions
    
    async def auto_optimize(self, chat_system, cache_manager, ai_optimizer):
        """Automatically apply optimizations based on bottlenecks."""
        for bottleneck in self.bottlenecks:
            if bottleneck.severity == 'critical':
                await self._apply_critical_optimization(bottleneck, chat_system, cache_manager, ai_optimizer)
            elif bottleneck.severity == 'high':
                await self._apply_high_priority_optimization(bottleneck, chat_system, cache_manager, ai_optimizer)
    
    async def _apply_critical_optimization(self, bottleneck: Bottleneck, chat_system, cache_manager, ai_optimizer):
        """Apply critical optimizations immediately."""
        if bottleneck.component == 'system' and bottleneck.metric == 'memory_usage':
            # Force cache cleanup
            await cache_manager.emergency_cleanup()
            self.optimizations_applied.append(f"Emergency cache cleanup for {bottleneck.description}")
        
        elif bottleneck.component == 'chat_system' and bottleneck.metric == 'response_time':
            # Enable aggressive optimizations
            chat_system.enable_streaming = True
            ai_optimizer.enable_batching = True
            self.optimizations_applied.append(f"Enabled streaming and batching for {bottleneck.description}")
    
    async def _apply_high_priority_optimization(self, bottleneck: Bottleneck, chat_system, cache_manager, ai_optimizer):
        """Apply high priority optimizations."""
        if bottleneck.component == 'cache_manager':
            # Optimize cache settings
            await cache_manager.optimize_settings()
            self.optimizations_applied.append(f"Optimized cache settings for {bottleneck.description}")
        
        elif bottleneck.component == 'ai_api':
            # Implement circuit breaker
            ai_optimizer.enable_circuit_breaker = True
            self.optimizations_applied.append(f"Enabled circuit breaker for {bottleneck.description}")