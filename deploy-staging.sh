#!/bin/bash

set -e

echo "🚀 Starting staging deployment..."

# Validate environment file exists
if [ ! -f ".env.staging" ]; then
    echo "❌ Error: .env.staging file not found"
    exit 1
fi

# Load environment variables
export $(cat .env.staging | grep -v '^#' | xargs)

# Validate required variables
required_vars=("DB_NAME" "DB_USER" "DB_PASSWORD" "API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Required environment variable $var is not set"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Create monitoring directories
mkdir -p monitoring/grafana/{dashboards,datasources}

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.staging.yml --env-file .env.staging down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.staging.yml --env-file .env.staging up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health check
echo "🏥 Performing health checks..."
if curl -f http://localhost:${WEB_PORT:-3000}/health > /dev/null 2>&1; then
    echo "✅ Web service is healthy"
else
    echo "❌ Web service health check failed"
    docker-compose -f docker-compose.staging.yml logs web
    exit 1
fi

# Check database connection
if docker-compose -f docker-compose.staging.yml exec -T db pg_isready -U $DB_USER > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database health check failed"
    exit 1
fi

echo "🎉 Staging deployment completed successfully!"
echo "📊 Services available at:"
echo "   - Web App: http://localhost:${WEB_PORT:-3000}"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3001 (admin/${GRAFANA_PASSWORD})"