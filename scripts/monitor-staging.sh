#!/bin/bash

echo "📊 Staging Environment Status"
echo "=============================="

# Service status
echo "🔍 Service Status:"
docker-compose -f docker-compose.staging.yml ps

echo ""
echo "🏥 Health Check:"
curl -s http://localhost:3000/health | jq '.' || echo "Health endpoint unavailable"

echo ""
echo "📈 Quick Metrics:"
curl -s http://localhost:3000/metrics | grep -E "(http_requests_total|http_request_duration)" | head -5

echo ""
echo "💾 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"