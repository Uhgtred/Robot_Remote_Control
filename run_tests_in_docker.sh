#!/bin/bash
# Script to build and run Docker container for testing

set -e  # Exit on error

echo "Building Docker image..."
docker build -t robot-remote-control .

echo "Running tests in Docker container..."
docker run --rm robot-remote-control python3 /app/run_tests.py

echo "Tests completed."