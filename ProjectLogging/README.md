# ProjectLogging Package

## Overview
The ProjectLogging package provides a centralized logging mechanism for the Robot Remote Control project. It offers a simple and consistent way to create and manage logs throughout the application, with support for both file and console output.

## Components

### Core Classes
- **Logger**: The main class that handles log creation, formatting, and output. It supports customizable log levels, file paths, and console output options.

## Features
- Centralized logging configuration
- Support for both file and console logging
- Customizable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Automatic log file management (old logs are deleted to prevent storage issues)
- Consistent log formatting across the application

## Usage

### Basic Usage
```python
from ProjectLogging.Logger import Logger

# Create a logger with a specific name and log file
logger = Logger('MyComponent', 'my_component.log').getLogger

# Log messages at different levels
logger.debug('Detailed debugging information')
logger.info('General information about program execution')
logger.warning('Warning about potential issues')
logger.error('Error that occurred during execution')
logger.critical('Critical error that may cause program termination')
```

### Customizing Log Level and Console Output
```python
import logging
from ProjectLogging.Logger import Logger

# Create a logger with custom log level and no console output
logger = Logger(
    name='MyComponent',
    logFile='my_component.log',
    logLevel=logging.INFO,  # Only log INFO and above
    consoleOutput=False     # Disable console output
).getLogger

# Now only INFO and above will be logged, and only to the file
logger.debug('This will not be logged')  # Won't be logged (below INFO)
logger.info('This will be logged to file only')  # Logged to file only
```

## Log File Location
By default, log files are created in the ProjectLogging directory. The path is automatically determined based on the location of the Logger module.

## Log Format
Logs are formatted with a consistent pattern:
```
[Timestamp] - [LogLevel][LoggerName]: Message
```

Example:
```
12-05-2023 14:30:45 - [INFO][MyComponent]: System initialized successfully
```

## Integration
The ProjectLogging package is used throughout the Robot Remote Control project:

- **BusTransactions**: Logs communication events and errors
- **GUI**: Logs user interface actions and updates
- **SteeringInput**: Logs control commands and device status
- **Runners**: Logs process execution and status

## Best Practices
- Create a separate logger for each component or module
- Use appropriate log levels (DEBUG for detailed information, INFO for general status, etc.)
- Include relevant context in log messages
- Avoid logging sensitive information