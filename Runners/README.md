# Runners Package

## Overview
The Runners package provides mechanisms for executing tasks asynchronously or in separate threads in the Robot Remote Control project. It offers a flexible way to run operations that might block the main execution flow, ensuring responsive application behavior.

## Components

### Core Classes
- **Runner**: An abstract base class that defines the interface for all runner implementations.
- **AsyncRunner**: Implements the Runner interface using Python's asyncio for asynchronous task execution.
- **ThreadRunner**: Implements the Runner interface using Python's threading module for threaded task execution.

## Features
- Support for both asynchronous and threaded execution models
- Task management and monitoring
- Resource cleanup on program exit
- Flexible task scheduling

## Usage

### ThreadRunner
The ThreadRunner class is used for executing tasks in separate threads:

```python
from Runners.ThreadRunner import ThreadRunner

# Create a thread runner
runner = ThreadRunner()

# Define a task
def my_task(arg1, arg2):
    # Do something time-consuming
    print(f"Processing {arg1} and {arg2}")
    
# Add the task to the runner
runner.addTask(my_task, "value1", "value2")

# Run all tasks
runner.runTasks()

# Stop task execution (if needed)
runner.stopTasks()
```

### AsyncRunner
The AsyncRunner class is used for executing tasks asynchronously:

```python
from Runners.AsyncRunner import AsyncRunner

# Create an async runner
runner = AsyncRunner()

# Define a task
def my_async_task(arg1, arg2):
    # Do something time-consuming
    print(f"Processing {arg1} and {arg2}")
    return "Task completed"
    
# Add the task to the runner
runner.addTask(my_async_task, "value1", "value2")

# Run all tasks
runner.runTasks()

# Stop task execution (if needed)
runner.stopTasks()
```

## Integration
The Runners package is used throughout the Robot Remote Control project:

- **BusTransactions**: For handling communication operations without blocking
- **GUI**: For updating the user interface while processing data
- **SteeringInput**: For processing input commands in the background

## Best Practices
- Use ThreadRunner for CPU-bound tasks
- Use AsyncRunner for I/O-bound tasks
- Always call stopTasks() when done to ensure proper resource cleanup
- Avoid sharing mutable state between tasks without proper synchronization