-- Common performance indexes for typical web application

-- User lookup optimizations
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_users_active_created ON users(is_active, created_at DESC);

-- Product/content search optimizations
CREATE INDEX CONCURRENTLY idx_products_category_price ON products(category_id, price);
CREATE INDEX CONCURRENTLY idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
CREATE INDEX CONCURRENTLY idx_products_active_updated ON products(is_active, updated_at DESC);

-- Order/transaction optimizations
CREATE INDEX CONCURRENTLY idx_orders_user_status ON orders(user_id, status);
CREATE INDEX CONCURRENTLY idx_orders_created_status ON orders(created_at DESC, status);

-- Composite indexes for common query patterns
CREATE INDEX CONCURRENTLY idx_order_items_order_product ON order_items(order_id, product_id);

-- Partial indexes for common filtered queries
CREATE INDEX CONCURRENTLY idx_users_active_email ON users(email) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_products_available ON products(category_id, price) WHERE is_active = true AND stock > 0;