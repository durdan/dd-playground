#!/bin/bash

SERVICE=${1:-web}

echo "📋 Showing logs for service: $SERVICE"
docker-compose -f docker-compose.staging.yml logs -f $SERVICE