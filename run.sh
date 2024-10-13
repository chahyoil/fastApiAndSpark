#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "Starting build and run process at $(date)"

echo "Building Docker image..."
docker build -t f1-race-data-api .

echo "Stopping and removing any existing containers..."
docker stop f1-race-data-api-container 2>/dev/null || true
docker rm f1-race-data-api-container 2>/dev/null || true

echo "Starting new container..."
docker run -d --name f1-race-data-api-container -p 8000:8000 f1-race-data-api

echo "Checking container status..."
sleep 5
if [ "$(docker inspect -f '{{.State.Running}}' f1-race-data-api-container 2>/dev/null)" = "true" ]; then
    echo "Container is running successfully."
    echo "Access the API at http://localhost:8000"
else
    echo "Container failed to start. Check logs for details."
    docker logs f1-race-data-api-container
    exit 1
fi

echo "Build and run process completed at $(date)"
