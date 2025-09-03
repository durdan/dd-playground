from flask import Flask, request, jsonify
from services.query_optimizer import QueryOptimizer, CacheManager
from database.connection_pool import DatabasePool
import redis
import time

app = Flask(__name__)

# Initialize components
db_pool = DatabasePool("postgresql://user:pass@localhost/db")
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache_manager = CacheManager(redis_client)
query_optimizer = QueryOptimizer(db_pool, redis_client)

def track_response_time(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        response_time = (time.time() - start_time) * 1000
        
        # Log if over 200ms threshold
        if response_time > 200:
            print(f"WARNING: {f.__name__} took {response_time:.2f}ms")
        
        return result
    return wrapper

@app.route('/api/users/<int:user_id>/orders')
@track_response_time
def get_user_orders(user_id):
    try:
        result = query_optimizer.get_user_with_orders(user_id)
        
        if not result.data:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'data': result.data,
            'meta': {
                'execution_time_ms': result.execution_time,
                'cache_hit': result.cache_hit
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/search')
@track_response_time
def search_products():
    try:
        # Extract query parameters
        category_id = request.args.get('category_id', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search_term = request.args.get('q')
        limit = min(request.args.get('limit', 20, type=int), 100)  # Cap at 100
        offset = request.args.get('offset', 0, type=int)
        
        result = query_optimizer.search_products(
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            search_term=search_term,
            limit=limit,
            offset=offset
        )
        
        return jsonify({
            'data': result.data,
            'meta': {
                'execution_time_ms': result.execution_time,
                'limit': limit,
                'offset': offset
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/performance')
def performance_stats():
    return jsonify(db_pool.stats)