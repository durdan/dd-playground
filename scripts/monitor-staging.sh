#!/bin/bash

echo "📊 Staging Environment Monitoring"
echo "=================================="

# Check container status
echo "🐳 Container Status:"
docker-compose -f docker-compose.staging.yml ps

echo ""
echo "🔍 Health Checks:"

# Web service health
if curl -s http://localhost:8080/health | jq -r '.status' | grep -q "healthy"; then
    echo "✅ Web Service: Healthy"
else
    echo "❌ Web Service: Unhealthy"
fi

# Database connection
if docker-compose -f docker-compose.staging.yml exec -T postgres pg_isready -U staging_user > /dev/null 2>&1; then
    echo "✅ PostgreSQL: Connected"
else
    echo "❌ PostgreSQL: Connection failed"
fi

# Redis connection
if docker-compose -f docker-compose.staging.yml exec -T redis redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis: Connected"
else
    echo "❌ Redis: Connection failed"
fi

echo ""
echo "📈 Quick Metrics:"
echo "Uptime: $(curl -s http://localhost:8080/health | jq -r '.uptime' | cut -d. -f1)s"
echo "Environment: $(curl -s http://localhost:8080/health | jq -r '.environment')"

echo ""
echo "🔗 Monitoring URLs:"
echo "Application: http://localhost:8080"
echo "Health Check: http://localhost:8080/health"
echo "Metrics: http://localhost:8080/metrics"
echo "Grafana: http://localhost:3000"
echo "Prometheus: http://localhost:9090"