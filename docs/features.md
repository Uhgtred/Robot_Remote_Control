# Features

## Communication
The Robot Remote Control project provides robust communication capabilities through the BusTransactions package:

- Support for multiple communication protocols (Ethernet, Serial)
- Layered architecture for message processing (compression, encoding, serialization)
- Plugin system for easy extension with new communication methods

## User Interface
The GUI package offers a comprehensive user interface for controlling the robot:

- Real-time video display from robot cameras
- Control interface for robot movement
- Status monitoring and feedback

## Event System
The Events package implements an event-driven architecture:

- Decoupled communication between components
- Support for multiple subscribers per event
- Centralized event management

## Logging
The ProjectLogging package provides a centralized logging mechanism:

- Support for both file and console logging
- Customizable log levels
- Automatic log file management

## Task Execution
The Runners package manages asynchronous and threaded task execution:

- Support for both threaded and asynchronous execution models
- Task management and monitoring
- Resource cleanup on program exit

## Input Processing
The SteeringInput package processes input from various steering devices:

- Support for different input devices (keyboard, gamepad, etc.)
- Configurable input mapping
- Real-time input processing