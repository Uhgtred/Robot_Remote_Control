# Robot Remote Control

Welcome to the documentation for the Robot Remote Control project. This software is designed to remotely control a robot for the HomeExplorer project.

## Project Overview

The Robot Remote Control project is a comprehensive software solution for controlling robots remotely. It provides a flexible architecture with the following key features:

- Communication over various bus systems (Ethernet, Serial, etc.)
- Event-driven architecture for decoupled component interaction
- Graphical user interface for robot control and video display
- Configurable steering input mechanisms
- Comprehensive logging system

## Package Structure

The project is organized into several packages, each with its own specific responsibility:

- **BusTransactions**: Handles communication over various bus systems
- **Configurations**: Manages configuration settings
- **Events**: Implements an event-driven architecture
- **GUI**: Provides the graphical user interface
- **ProjectLogging**: Handles logging throughout the application
- **Runners**: Manages asynchronous and threaded task execution
- **SteeringInput**: Processes input from steering devices

## Getting Started

To get started with the Robot Remote Control project, see the [Setup](setup.md) page for installation instructions and the [Features](features.md) page for an overview of available functionality.
