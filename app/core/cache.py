import redis.asyncio as redis
from typing import Optional, Any
import json
import pickle
from .config import settings

class CacheManager:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        
    async def init_redis(self):
        """Initialize Redis connection"""
        if settings.REDIS_URL:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            
    async def close_redis(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
            
        try:
            value = await self.redis_client.get(key)
            if value:
                return pickle.loads(value)
        except Exception:
            return None
        return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        if not self.redis_client:
            return False
            
        try:
            ttl = ttl or settings.CACHE_TTL
            serialized_value = pickle.dumps(value)
            await self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis_client:
            return False
            
        try:
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis_client:
            return False
            
        try:
            return await self.redis_client.exists(key) > 0
        except Exception:
            return False

# Global cache instance
cache = CacheManager()