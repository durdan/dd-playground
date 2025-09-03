#!/bin/bash

echo "📊 Staging Environment Status"
echo "=============================="

# Check if services are running
echo "🔍 Service Status:"
docker-compose -f docker-compose.staging.yml ps

echo ""
echo "🏥 Health Checks:"

# Web app health
if curl -s http://localhost:3000/health | jq -r '.status' 2>/dev/null; then
    echo "✅ Web App: Healthy"
else
    echo "❌ Web App: Unhealthy"
fi

# Database health
if docker-compose -f docker-compose.staging.yml exec -T db pg_isready -U staginguser > /dev/null 2>&1; then
    echo "✅ Database: Healthy"
else
    echo "❌ Database: Unhealthy"
fi

# Redis health
if docker-compose -f docker-compose.staging.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Healthy"
else
    echo "❌ Redis: Unhealthy"
fi

echo ""
echo "📈 Quick Metrics:"
echo "Memory Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"