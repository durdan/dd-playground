#!/bin/bash

echo "📊 Staging Environment Status"
echo "=============================="

# Check service health
services=("web" "postgres" "redis" "prometheus" "grafana")

for service in "${services[@]}"; do
    if docker-compose -f docker-compose.staging.yml ps $service | grep -q "Up"; then
        echo "✅ $service: Running"
    else
        echo "❌ $service: Not running"
    fi
done

echo ""
echo "🏥 Application Health Check:"
if curl -s http://localhost:8080/health | jq -r '.status' | grep -q "healthy"; then
    echo "✅ Application: Healthy"
else
    echo "❌ Application: Unhealthy"
fi

echo ""
echo "📈 Quick Metrics:"
curl -s http://localhost:8080/api/status | jq '.'