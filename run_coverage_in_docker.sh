#!/bin/bash
# Script to build and run Docker container for testing with coverage

set -e  # Exit on error

echo "Building Docker image..."
docker build -t robot_image .

echo "Running tests with coverage in Docker container..."
docker run --name coverage_container robot_image sh -c "python -m coverage run --rcfile=.coveragerc -m unittest discover -v && python -m coverage xml --rcfile=.coveragerc -o /app/coverage.xml && python -m coverage report --rcfile=.coveragerc"

echo "Copying coverage report from container..."
docker cp coverage_container:/app/coverage.xml ./coverage.xml

echo "Cleaning up container..."
docker rm coverage_container

echo "Coverage tests completed. Report saved to coverage.xml"