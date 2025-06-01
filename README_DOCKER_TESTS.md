# Running Tests in Docker

This document provides instructions on how to run all tests for the Robot Remote Control project inside a Docker container.

## Prerequisites

- Docker installed on your system
- Basic knowledge of Docker commands

## Files

- `run_tests.py`: A Python script that runs all tests using pytest and collects coverage data.
- `run_tests_in_docker.sh`: A shell script that builds the Docker image and runs the tests inside a container.
- `run_coverage_in_docker.sh`: A shell script that builds the Docker image, runs tests with coverage using unittest, and copies the coverage report to the host.

## Running Tests

1. Make sure all scripts are executable:
   ```bash
   chmod +x run_tests.py run_tests_in_docker.sh run_coverage_in_docker.sh
   ```

2. Run the tests in Docker:
   ```bash
   ./run_tests_in_docker.sh
   ```

3. The script will:
   - Build a Docker image using the Dockerfile in the project
   - Run a container from that image
   - Execute the `run_tests.py` script inside the container
   - Display the test results

4. Alternatively, you can run tests with coverage using the provided script:
   ```bash
   ./run_coverage_in_docker.sh
   ```

   This script:
   - Builds the Docker image
   - Runs all unittest tests with coverage
   - Generates an XML coverage report and copies it to ./coverage.xml
   - Displays a coverage report in the console
   - Cleans up the container

5. If you prefer to run the coverage command manually:
   ```bash
   docker run --name coverage_container robot_image sh -c "python -m coverage run --rcfile=.coveragerc -m unittest discover -v && python -m coverage xml --rcfile=.coveragerc -o /app/coverage.xml && python -m coverage report --rcfile=.coveragerc"
   ```

## Test Results

After running the tests, you can find a detailed report in `test_results_report.md`. This report includes:
- A summary of test results (passed, failed, errors)
- Test coverage information
- Identified issues
- Recommendations for fixing failing tests

## Troubleshooting

If you encounter any issues:

1. **Docker Build Fails**:
   - Check if Docker is running
   - Ensure you have the necessary permissions to build Docker images
   - Verify that the Dockerfile is correctly formatted

2. **Tests Fail**:
   - Some tests may fail due to environment-specific issues in Docker
   - Network-related tests might fail due to IP address binding issues
   - Check the test results report for specific recommendations

## Notes

- The Docker container is configured with a dummy display for headless execution
- The container exposes port 2000 for communication
- All dependencies are installed in a Python virtual environment inside the container
