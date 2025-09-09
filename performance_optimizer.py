import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from collections import deque
import weakref
import gc

@dataclass
class PerformanceMetrics:
    render_time: float = 0.0
    memory_usage: int = 0
    items_rendered: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    def reset(self):
        self.render_time = 0.0
        self.memory_usage = 0
        self.items_rendered = 0
        self.cache_hits = 0
        self.cache_misses = 0

class MemoryManager:
    def __init__(self, max_cache_size: int = 1000):
        self.max_cache_size = max_cache_size
        self.cache = {}
        self.access_order = deque()
        self.weak_refs = weakref.WeakSet()
    
    def cache_item(self, key: str, item: Any) -> None:
        if len(self.cache) >= self.max_cache_size:
            self._evict_oldest()
        
        self.cache[key] = item
        self.access_order.append(key)
    
    def get_cached_item(self, key: str) -> Optional[Any]:
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def _evict_oldest(self) -> None:
        if self.access_order:
            oldest_key = self.access_order.popleft()
            self.cache.pop(oldest_key, None)
    
    def cleanup(self) -> None:
        # Force garbage collection
        gc.collect()
        
        # Clear weak references
        self.weak_refs.clear()
        
        # Clear half of cache if it's getting large
        if len(self.cache) > self.max_cache_size * 0.8:
            items_to_remove = len(self.cache) // 2
            for _ in range(items_to_remove):
                if self.access_order:
                    key = self.access_order.popleft()
                    self.cache.pop(key, None)

class LazyLoader:
    def __init__(self, chunk_size: int = 50, preload_threshold: int = 10):
        self.chunk_size = chunk_size
        self.preload_threshold = preload_threshold
        self.loaded_chunks = {}
        self.loading_chunks = set()
        self.data_source = None
    
    def set_data_source(self, data_source: Callable[[int, int], List[Any]]) -> None:
        self.data_source = data_source
    
    async def load_chunk(self, chunk_index: int) -> List[Any]:
        if chunk_index in self.loaded_chunks:
            return self.loaded_chunks[chunk_index]
        
        if chunk_index in self.loading_chunks:
            # Wait for ongoing load
            while chunk_index in self.loading_chunks:
                await asyncio.sleep(0.01)
            return self.loaded_chunks.get(chunk_index, [])
        
        self.loading_chunks.add(chunk_index)
        
        try:
            start_idx = chunk_index * self.chunk_size
            end_idx = start_idx + self.chunk_size
            
            if self.data_source:
                chunk_data = await asyncio.to_thread(
                    self.data_source, start_idx, end_idx
                )
            else:
                chunk_data = []
            
            self.loaded_chunks[chunk_index] = chunk_data
            return chunk_data
        
        finally:
            self.loading_chunks.discard(chunk_index)
    
    async def get_items(self, start_index: int, count: int) -> List[Any]:
        items = []
        current_index = start_index
        remaining = count
        
        while remaining > 0:
            chunk_index = current_index // self.chunk_size
            chunk_offset = current_index % self.chunk_size
            
            chunk_data = await self.load_chunk(chunk_index)
            
            # Preload next chunk if we're close to the end
            if (chunk_offset >= self.chunk_size - self.preload_threshold and 
                chunk_index + 1 not in self.loaded_chunks):
                asyncio.create_task(self.load_chunk(chunk_index + 1))
            
            available_in_chunk = len(chunk_data) - chunk_offset
            take_count = min(remaining, available_in_chunk)
            
            if take_count > 0:
                items.extend(chunk_data[chunk_offset:chunk_offset + take_count])
                current_index += take_count
                remaining -= take_count
            else:
                break
        
        return items

class RenderOptimizer:
    def __init__(self, viewport_height: int = 600, item_height: int = 100):
        self.viewport_height = viewport_height
        self.item_height = item_height
        self.visible_range = (0, 0)
        self.render_buffer = 5  # Extra items to render outside viewport
        self.render_cache = {}
        self.pending_renders = set()
    
    def calculate_visible_range(self, scroll_position: int, total_items: int) -> tuple[int, int]:
        items_per_viewport = self.viewport_height // self.item_height
        
        start_index = max(0, (scroll_position // self.item_height) - self.render_buffer)
        end_index = min(
            total_items,
            start_index + items_per_viewport + (2 * self.render_buffer)
        )
        
        self.visible_range = (start_index, end_index)
        return self.visible_range
    
    async def render_items_batch(self, items: List[Any], renderer: Callable) -> List[Any]:
        batch_size = 10
        rendered_items = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_rendered = []
            
            for item in batch:
                item_id = getattr(item, 'id', str(hash(str(item))))
                
                if item_id in self.render_cache:
                    batch_rendered.append(self.render_cache[item_id])
                else:
                    rendered = await asyncio.to_thread(renderer, item)
                    self.render_cache[item_id] = rendered
                    batch_rendered.append(rendered)
            
            rendered_items.extend(batch_rendered)
            
            # Yield control to prevent blocking
            await asyncio.sleep(0)
        
        return rendered_items
    
    def cleanup_render_cache(self, visible_items: set) -> None:
        # Remove items not currently visible from cache
        keys_to_remove = [
            key for key in self.render_cache.keys()
            if key not in visible_items
        ]
        
        for key in keys_to_remove[:len(keys_to_remove)//2]:  # Remove half
            self.render_cache.pop(key, None)

class PerformanceOptimizer:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.lazy_loader = LazyLoader()
        self.render_optimizer = RenderOptimizer()
        self.metrics = PerformanceMetrics()
        self.optimization_tasks = []
    
    def analyze_performance(self) -> Dict[str, Any]:
        return {
            'render_time': self.metrics.render_time,
            'memory_usage': self.metrics.memory_usage,
            'cache_efficiency': (
                self.metrics.cache_hits / 
                max(1, self.metrics.cache_hits + self.metrics.cache_misses)
            ),
            'items_rendered': self.metrics.items_rendered,
            'recommendations': self._get_recommendations()
        }
    
    def _get_recommendations(self) -> List[str]:
        recommendations = []
        
        if self.metrics.render_time > 100:  # ms
            recommendations.append("Consider reducing render complexity")
        
        cache_efficiency = (
            self.metrics.cache_hits / 
            max(1, self.metrics.cache_hits + self.metrics.cache_misses)
        )
        if cache_efficiency < 0.7:
            recommendations.append("Improve caching strategy")
        
        if self.metrics.memory_usage > 100 * 1024 * 1024:  # 100MB
            recommendations.append("Reduce memory usage")
        
        return recommendations
    
    async def optimize_chat_rendering(
        self, 
        messages: List[Any], 
        scroll_position: int,
        renderer: Callable
    ) -> List[Any]:
        start_time = time.time()
        
        # Calculate visible range
        visible_start, visible_end = self.render_optimizer.calculate_visible_range(
            scroll_position, len(messages)
        )
        
        # Load visible items lazily
        visible_messages = await self.lazy_loader.get_items(
            visible_start, visible_end - visible_start
        )
        
        # Render with optimization
        rendered_messages = await self.render_optimizer.render_items_batch(
            visible_messages, renderer
        )
        
        # Update metrics
        self.metrics.render_time = (time.time() - start_time) * 1000
        self.metrics.items_rendered = len(rendered_messages)
        
        # Schedule cleanup
        self._schedule_cleanup()
        
        return rendered_messages
    
    def _schedule_cleanup(self) -> None:
        async def cleanup_task():
            await asyncio.sleep(5)  # Wait 5 seconds
            self.memory_manager.cleanup()
            visible_items = set(
                str(i) for i in range(
                    self.render_optimizer.visible_range[0],
                    self.render_optimizer.visible_range[1]
                )
            )
            self.render_optimizer.cleanup_render_cache(visible_items)
        
        task = asyncio.create_task(cleanup_task())
        self.optimization_tasks.append(task)
        
        # Clean up completed tasks
        self.optimization_tasks = [
            t for t in self.optimization_tasks if not t.done()
        ]

class ChatUIOptimizer:
    def __init__(self):
        self.performance_optimizer = PerformanceOptimizer()
        self.is_optimizing = False
    
    def setup_data_source(self, data_source: Callable[[int, int], List[Any]]) -> None:
        self.performance_optimizer.lazy_loader.set_data_source(data_source)
    
    async def render_chat_messages(
        self,
        total_messages: int,
        scroll_position: int,
        message_renderer: Callable
    ) -> Dict[str, Any]:
        if self.is_optimizing:
            return {'messages': [], 'status': 'optimizing'}
        
        self.is_optimizing = True
        
        try:
            # Create dummy messages for the visible range
            visible_start, visible_end = (
                self.performance_optimizer.render_optimizer
                .calculate_visible_range(scroll_position, total_messages)
            )
            
            # Simulate message loading
            messages = [
                {'id': i, 'content': f'Message {i}', 'timestamp': time.time()}
                for i in range(visible_start, visible_end)
            ]
            
            rendered_messages = await (
                self.performance_optimizer.optimize_chat_rendering(
                    messages, scroll_position, message_renderer
                )
            )
            
            performance_data = self.performance_optimizer.analyze_performance()
            
            return {
                'messages': rendered_messages,
                'visible_range': (visible_start, visible_end),
                'performance': performance_data,
                'status': 'optimized'
            }
        
        finally:
            self.is_optimizing = False
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        return self.performance_optimizer.analyze_performance()
    
    async def preload_specs(self, spec_ids: List[str]) -> None:
        """Preload large specifications in the background"""
        async def load_spec(spec_id: str):
            # Simulate spec loading
            await asyncio.sleep(0.1)
            spec_data = {'id': spec_id, 'content': f'Large spec {spec_id}'}
            self.performance_optimizer.memory_manager.cache_item(
                f'spec_{spec_id}', spec_data
            )
        
        tasks = [load_spec(spec_id) for spec_id in spec_ids]
        await asyncio.gather(*tasks)