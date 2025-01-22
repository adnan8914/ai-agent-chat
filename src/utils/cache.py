import redis
from typing import Any, Optional
import pickle
import hashlib
from datetime import timedelta

class CacheManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )
        
    def generate_key(self, prefix: str, data: Any) -> str:
        """Generate a unique cache key"""
        data_str = str(data)
        return f"{prefix}:{hashlib.md5(data_str.encode()).hexdigest()}"
    
    def set(self, key: str, value: Any, expire_in: Optional[int] = None):
        """Store value in cache"""
        try:
            serialized_value = pickle.dumps(value)
            self.redis_client.set(key, serialized_value)
            if expire_in:
                self.redis_client.expire(key, expire_in)
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None 