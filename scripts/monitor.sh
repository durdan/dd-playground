#!/bin/bash

# Simple monitoring script
check_service() {
    local service=$1
    local url=$2
    
    if curl -f -s "$url" > /dev/null; then
        echo "✅ $service is healthy"
    else
        echo "❌ $service is down"
        return 1
    fi
}

echo "=== Service Health Check ==="
check_service "Web Application" "http://localhost:3000/health"
check_service "Prometheus" "http://localhost:9090/-/healthy"
check_service "Grafana" "http://localhost:3001/api/health"

echo ""
echo "=== Container Status ==="
docker-compose -f docker-compose.staging.yml ps