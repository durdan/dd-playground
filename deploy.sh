#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}
ENV_FILE=".env.${ENVIRONMENT}"

echo "Deploying to ${ENVIRONMENT} environment..."

# Validate environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file $ENV_FILE not found"
    exit 1
fi

# Load environment variables
export $(cat $ENV_FILE | grep -v '^#' | xargs)

# Build and deploy
echo "Building application..."
docker-compose -f docker-compose.staging.yml --env-file $ENV_FILE build

echo "Starting services..."
docker-compose -f docker-compose.staging.yml --env-file $ENV_FILE up -d

echo "Waiting for services to be healthy..."
sleep 10

# Health checks
echo "Checking application health..."
curl -f http://localhost:${WEB_PORT:-3000}/health || {
    echo "Health check failed"
    docker-compose -f docker-compose.staging.yml logs web
    exit 1
}

echo "Deployment completed successfully!"
echo "Application: http://localhost:${WEB_PORT:-3000}"
echo "Grafana: http://localhost:3001 (admin/${GRAFANA_PASSWORD})"
echo "Prometheus: http://localhost:9090"