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
echo "📦 Building services..."
docker-compose -f docker-compose.staging.yml build

echo "🔄 Stopping existing services..."
docker-compose -f docker-compose.staging.yml down

echo "🚀 Starting services..."
docker-compose -f docker-compose.staging.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health check
echo "🏥 Checking service health..."
if curl -f http://localhost:${WEB_PORT:-3000}/health > /dev/null 2>&1; then
    echo "✅ Staging deployment successful!"
    echo "🌐 Application: http://localhost:${WEB_PORT:-3000}"
    echo "📊 Grafana: http://localhost:3001 (admin/${GRAFANA_PASSWORD})"
    echo "📈 Prometheus: http://localhost:9090"
else
    echo "❌ Health check failed"
    docker-compose -f docker-compose.staging.yml logs
    exit 1
fi