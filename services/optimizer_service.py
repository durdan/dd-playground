import asyncio
import hashlib
import os
from typing import Optional, Callable, Any
from functools import wraps
import time

class OptimizerService:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, spec_id: str, format_type: str, version: str) -> str:
        """Generate cache key for specification export"""
        content = f"{spec_id}:{format_type}:{version}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_file(self, cache_key: str) -> Optional[str]:
        """Check if cached export file exists"""
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.cache")
        if os.path.exists(cache_path):
            return cache_path
        return None
    
    def cache_file(self, cache_key: str, file_path: str) -> None:
        """Cache the generated file"""
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.cache")
        if os.path.exists(file_path):
            os.rename(file_path, cache_path)
    
    async def optimize_export(self, export_func: Callable, *args, **kwargs) -> Any:
        """Run export function asynchronously for better performance"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, export_func, *args, **kwargs)
    
    def performance_monitor(self, func: Callable) -> Callable:
        """Decorator to monitor export performance"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Export completed in {end_time - start_time:.2f} seconds")
            return result
        return wrapper