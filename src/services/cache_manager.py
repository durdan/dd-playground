import os
import json
import hashlib
import time
from typing import Optional, Dict, Any
from pathlib import Path

class CacheManager:
    def __init__(self, cache_dir: str = "cache", ttl_seconds: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self.cache_dir.mkdir(exist_ok=True)
    
    def _generate_cache_key(self, specification: Dict[str, Any], format_type: str) -> str:
        """Generate cache key from specification content and format."""
        content = json.dumps(specification, sort_keys=True)
        return hashlib.md5(f"{content}_{format_type}".encode()).hexdigest()
    
    def get_cached_file(self, specification: Dict[str, Any], format_type: str) -> Optional[str]:
        """Retrieve cached file if exists and not expired."""
        cache_key = self._generate_cache_key(specification, format_type)
        cache_file = self.cache_dir / f"{cache_key}.{format_type}"
        metadata_file = self.cache_dir / f"{cache_key}.meta"
        
        if not cache_file.exists() or not metadata_file.exists():
            return None
        
        # Check TTL
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            if time.time() - metadata['created_at'] > self.ttl_seconds:
                self._cleanup_cache_entry(cache_key, format_type)
                return None
            
            return str(cache_file)
        except (json.JSONDecodeError, KeyError, OSError):
            return None
    
    def cache_file(self, specification: Dict[str, Any], format_type: str, file_path: str) -> None:
        """Cache generated file with metadata."""
        cache_key = self._generate_cache_key(specification, format_type)
        cache_file = self.cache_dir / f"{cache_key}.{format_type}"
        metadata_file = self.cache_dir / f"{cache_key}.meta"
        
        try:
            # Copy file to cache
            import shutil
            shutil.copy2(file_path, cache_file)
            
            # Save metadata
            metadata = {
                'created_at': time.time(),
                'original_path': file_path,
                'format': format_type
            }
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f)
        except OSError as e:
            print(f"Failed to cache file: {e}")
    
    def _cleanup_cache_entry(self, cache_key: str, format_type: str) -> None:
        """Remove cache entry and metadata."""
        cache_file = self.cache_dir / f"{cache_key}.{format_type}"
        metadata_file = self.cache_dir / f"{cache_key}.meta"
        
        for file in [cache_file, metadata_file]:
            if file.exists():
                try:
                    file.unlink()
                except OSError:
                    pass
    
    def clear_expired_cache(self) -> int:
        """Remove all expired cache entries. Returns count of removed entries."""
        removed_count = 0
        current_time = time.time()
        
        for metadata_file in self.cache_dir.glob("*.meta"):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                if current_time - metadata['created_at'] > self.ttl_seconds:
                    cache_key = metadata_file.stem
                    format_type = metadata.get('format', 'unknown')
                    self._cleanup_cache_entry(cache_key, format_type)
                    removed_count += 1
            except (json.JSONDecodeError, KeyError, OSError):
                continue
        
        return removed_count