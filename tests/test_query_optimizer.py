import unittest
from unittest.mock import Mock, patch
from services.query_optimizer import QueryOptimizer, CacheManager

class TestQueryOptimizer(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_cache = Mock()
        self.optimizer = QueryOptimizer(self.mock_db, self.mock_cache)
    
    def test_get_user_with_orders_cache_hit(self):
        # Setup cache hit
        self.mock_cache.get.return_value = {'id': 1, 'orders': []}
        
        result = self.optimizer.get_user_with_orders(1)
        
        self.assertIsNotNone(result.data)
        self.mock_cache.get.assert_called_once()
        self.mock_db.execute.assert_not_called()
    
    def test_get_user_with_orders_cache_miss(self):
        # Setup cache miss
        self.mock_cache.get.return_value = None
        self.mock_db.execute.return_value.fetchone.return_value = {'id': 1, 'orders': []}
        
        result = self.optimizer.get_user_with_orders(1)
        
        self.assertIsNotNone(result.data)
        self.mock_cache.get.assert_called_once()
        self.mock_db.execute.assert_called_once()
        self.mock_cache.setex.assert_called_once()
    
    def test_search_products_with_filters(self):
        self.mock_db.execute.return_value.fetchall.return_value = [
            {'id': 1, 'name': 'Product 1', 'price': 10.0}
        ]
        
        result = self.optimizer.search_products(
            category_id=1, 
            min_price=5.0, 
            max_price=15.0,
            search_term='test'
        )
        
        self.assertIsNotNone(result.data)
        self.mock_db.execute.assert_called_once()
        
        # Verify query contains all conditions
        call_args = self.mock_db.execute.call_args[0]
        query = call_args[0]
        self.assertIn('category_id = %s', query)
        self.assertIn('price >= %s', query)
        self.assertIn('price <= %s', query)
        self.assertIn('name ILIKE %s', query)

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.mock_redis = Mock()
        self.cache_manager = CacheManager(self.mock_redis)
    
    def test_get_or_set_cache_hit(self):
        self.mock_redis.get.return_value = 'cached_value'
        fetch_func = Mock()
        
        result = self.cache_manager.get_or_set('key', fetch_func)
        
        self.assertEqual(result, 'cached_value')
        fetch_func.assert_not_called()
    
    def test_get_or_set_cache_miss(self):
        self.mock_redis.get.return_value = None
        fetch_func = Mock(return_value='fresh_value')
        
        result = self.cache_manager.get_or_set('key', fetch_func, ttl=300)
        
        self.assertEqual(result, 'fresh_value')
        fetch_func.assert_called_once()
        self.mock_redis.setex.assert_called_once_with('key', 300, 'fresh_value')