#!/bin/bash

echo "📊 Staging Environment Status"
echo "================================"

docker-compose -f docker-compose.staging.yml ps

echo ""
echo "🏥 Health Checks:"
echo "--------------------------------"

# Application health
if curl -s http://localhost:8080/health | jq -r '.status' 2>/dev/null; then
    echo "✅ Application: Healthy"
else
    echo "❌ Application: Unhealthy"
fi

# Prometheus health
if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "✅ Prometheus: Healthy"
else
    echo "❌ Prometheus: Unhealthy"
fi

# Grafana health
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✅ Grafana: Healthy"
else
    echo "❌ Grafana: Unhealthy"
fi