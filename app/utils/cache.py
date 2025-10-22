"""
Simple caching utilities for FX data
"""

import time
from typing import Dict, Any, Optional

class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if time.time() - entry['timestamp'] > self.ttl:
            del self.cache[key]
            return None
        
        return entry['value']
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def clear(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
    
    def size(self) -> int:
        """Get number of cached entries"""
        return len(self.cache)

# Global cache instance
fx_cache = SimpleCache(ttl_seconds=300)  # 5 minutes TTL
