#!/bin/bash

set -e

cd "$(dirname "$0")"

LOG_FILE="docker_build_run.log"
echo "Starting build and run process at $(date)" > $LOG_FILE

echo "Building Docker image..."
docker build -t f1-race-data-api . 2>&1 | tee -a $LOG_FILE

echo "Stopping and removing any existing containers..."
docker stop f1-race-data-api-container 2>/dev/null || true
docker rm f1-race-data-api-container 2>/dev/null || true

echo "Starting new container..."
docker run -d --name f1-race-data-api-container -p 8000:8000 f1-race-data-api 2>&1 | tee -a $LOG_FILE

echo "Checking container status..."
sleep 5
if [ "$(docker inspect -f '{{.State.Running}}' f1-race-data-api-container 2>/dev/null)" = "true" ]; then
    echo "Container is running successfully." | tee -a $LOG_FILE
    echo "Access the API at http://localhost:8000" | tee -a $LOG_FILE
else
    echo "Container failed to start. Check logs for details." | tee -a $LOG_FILE
    docker logs f1-race-data-api-container 2>&1 | tee -a $LOG_FILE
    exit 1
fi

echo "Build and run process completed at $(date)" >> $LOG_FILE