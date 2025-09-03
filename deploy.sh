#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}
ENV_FILE=".env.${ENVIRONMENT}"

echo "Deploying to ${ENVIRONMENT} environment..."

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file $ENV_FILE not found"
    exit 1
fi

# Load environment variables
export $(cat $ENV_FILE | grep -v '^#' | xargs)

# Build and deploy
echo "Building services..."
docker-compose -f docker-compose.staging.yml --env-file $ENV_FILE build

echo "Starting services..."
docker-compose -f docker-compose.staging.yml --env-file $ENV_FILE up -d

echo "Waiting for services to be healthy..."
sleep 30

# Health check
echo "Performing health check..."
if curl -f http://localhost:${WEB_PORT:-3000}/health; then
    echo "✅ Deployment successful!"
    echo "🌐 Application: http://localhost:${WEB_PORT:-3000}"
    echo "📊 Grafana: http://localhost:3001 (admin/${GRAFANA_PASSWORD})"
    echo "📈 Prometheus: http://localhost:9090"
else
    echo "❌ Health check failed!"
    docker-compose -f docker-compose.staging.yml logs
    exit 1
fi