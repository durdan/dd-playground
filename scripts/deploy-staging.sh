#!/bin/bash

set -e

echo "🚀 Deploying to staging environment..."

# Load environment variables
if [ -f .env.staging ]; then
    export $(cat .env.staging | grep -v '^#' | xargs)
fi

# Build and deploy
echo "📦 Building application..."
docker-compose -f docker-compose.staging.yml build

echo "🔄 Stopping existing services..."
docker-compose -f docker-compose.staging.yml down

echo "🆙 Starting services..."
docker-compose -f docker-compose.staging.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health checks
echo "🏥 Checking application health..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Application is healthy"
else
    echo "❌ Application health check failed"
    exit 1
fi

echo "📊 Checking monitoring services..."
if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "✅ Prometheus is healthy"
else
    echo "⚠️  Prometheus health check failed"
fi

if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✅ Grafana is healthy"
else
    echo "⚠️  Grafana health check failed"
fi

echo "🎉 Staging deployment completed!"
echo "📱 Application: http://localhost:8080"
echo "📊 Prometheus: http://localhost:9090"
echo "📈 Grafana: http://localhost:3000 (admin/staging-grafana-pass)"