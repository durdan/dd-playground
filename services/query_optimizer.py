from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
from functools import wraps

@dataclass
class QueryResult:
    data: Any
    execution_time: float
    cache_hit: bool = False

class QueryOptimizer:
    def __init__(self, db_connection, cache_client=None):
        self.db = db_connection
        self.cache = cache_client
        self.query_stats = {}
    
    def measure_time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Log slow queries
            if execution_time > 100:  # Log queries over 100ms
                print(f"Slow query detected: {func.__name__} took {execution_time:.2f}ms")
            
            return QueryResult(data=result, execution_time=execution_time)
        return wrapper
    
    @measure_time
    def get_user_with_orders(self, user_id: int, limit: int = 10) -> Dict:
        """Optimized query to get user with recent orders"""
        cache_key = f"user_orders:{user_id}:{limit}"
        
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached
        
        # Single optimized query instead of N+1
        query = """
        SELECT 
            u.id, u.email, u.name,
            json_agg(
                json_build_object(
                    'id', o.id,
                    'total', o.total,
                    'status', o.status,
                    'created_at', o.created_at
                ) ORDER BY o.created_at DESC
            ) FILTER (WHERE o.id IS NOT NULL) as orders
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.id = %s
        GROUP BY u.id, u.email, u.name
        """
        
        result = self.db.execute(query, (user_id,)).fetchone()
        
        if result and self.cache:
            self.cache.setex(cache_key, 300, result)  # Cache for 5 minutes
        
        return result
    
    @measure_time
    def search_products(self, category_id: Optional[int] = None, 
                       min_price: Optional[float] = None,
                       max_price: Optional[float] = None,
                       search_term: Optional[str] = None,
                       limit: int = 20, offset: int = 0) -> List[Dict]:
        """Optimized product search with proper indexing"""
        
        conditions = ["is_active = true", "stock > 0"]
        params = []
        
        if category_id:
            conditions.append("category_id = %s")
            params.append(category_id)
        
        if min_price:
            conditions.append("price >= %s")
            params.append(min_price)
            
        if max_price:
            conditions.append("price <= %s")
            params.append(max_price)
        
        if search_term:
            conditions.append("name ILIKE %s")
            params.append(f"%{search_term}%")
        
        # Add pagination params
        params.extend([limit, offset])
        
        query = f"""
        SELECT id, name, price, category_id, stock, created_at
        FROM products 
        WHERE {' AND '.join(conditions)}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        
        return self.db.execute(query, params).fetchall()

class CacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get_or_set(self, key: str, fetch_func, ttl: int = 300):
        """Get from cache or fetch and cache the result"""
        cached = self.redis.get(key)
        if cached:
            return cached
        
        result = fetch_func()
        if result:
            self.redis.setex(key, ttl, result)
        return result
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)