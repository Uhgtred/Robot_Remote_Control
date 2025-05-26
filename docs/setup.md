# Setup

## Prerequisites
Before setting up the Robot Remote Control project, ensure you have the following prerequisites installed:

- Python 3.12 or higher
- pip (Python package manager)
- Git (for version control)

## Installation

### Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/Robot_Remote_Control.git
cd Robot_Remote_Control
```

### Install Dependencies
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Configuration
The project uses configuration files located in the `Configurations` package. You may need to adjust these settings based on your specific hardware and network setup.

## Running the Application
To run the main application:

```bash
python main.py
```

## Development Setup

### Setting Up a Development Environment
For development, it's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests
To run the unit tests:

```bash
python -m unittest discover -v
```

### Running with Coverage
To run tests with coverage:

```bash
python -m coverage run --source=. -m unittest discover -v
python -m coverage report -m
```

## Docker Setup
The project includes a Dockerfile for containerized deployment:

```bash
docker build -t robot_remote_control .
docker run -p 8000:8000 robot_remote_control
```

## Troubleshooting
If you encounter issues during setup or execution:

1. Check the logs in the `ProjectLogging` directory
2. Ensure all dependencies are correctly installed
3. Verify your hardware connections if using physical devices
4. Check network settings if using network communication