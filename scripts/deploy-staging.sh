#!/bin/bash

set -e

echo "🚀 Deploying to staging environment..."

# Load environment variables
if [ -f .env.staging ]; then
    export $(cat .env.staging | grep -v '^#' | xargs)
else
    echo "❌ .env.staging file not found"
    exit 1
fi

# Build and deploy
echo "📦 Building containers..."
docker-compose -f docker-compose.staging.yml build

echo "🔄 Stopping existing containers..."
docker-compose -f docker-compose.staging.yml down

echo "🚀 Starting services..."
docker-compose -f docker-compose.staging.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health checks
echo "🔍 Checking service health..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Web service is healthy"
else
    echo "❌ Web service health check failed"
    exit 1
fi

echo "📊 Services status:"
docker-compose -f docker-compose.staging.yml ps

echo "🎉 Staging deployment completed successfully!"
echo "📱 Application: http://localhost:8080"
echo "📊 Grafana: http://localhost:3000 (admin/staging-grafana-pass)"
echo "📈 Prometheus: http://localhost:9090"