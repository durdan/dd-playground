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
echo "📦 Building application..."
docker-compose -f docker-compose.staging.yml build

echo "🔄 Stopping existing services..."
docker-compose -f docker-compose.staging.yml down

echo "🆙 Starting services..."
docker-compose -f docker-compose.staging.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health check
echo "🏥 Checking application health..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Application is healthy"
else
    echo "❌ Application health check failed"
    docker-compose -f docker-compose.staging.yml logs web
    exit 1
fi

echo "📊 Monitoring URLs:"
echo "  - Application: http://localhost:8080"
echo "  - Grafana: http://localhost:3000 (admin/staging-grafana-pass)"
echo "  - Prometheus: http://localhost:9090"

echo "🎉 Staging deployment completed successfully!"