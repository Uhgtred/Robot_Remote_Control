# GUI Package

## Overview
The GUI package provides the graphical user interface components for the Robot Remote Control project. It follows the Model-View-Controller (MVC) architectural pattern to create a modular and maintainable user interface for controlling the robot and displaying video feeds.

## Components

### Core Classes
- **VideoGUI_Controller**: The main controller class that manages the video GUI application, initializing the root window, view, and model components.

### Subpackages
- **Models**: Contains data models that represent the application state and business logic
- **Views**: Contains view components that handle the visual representation of the GUI
- **RobotFrontend**: Contains the frontend code for the robot control interface

## Architecture
The GUI package follows the MVC architectural pattern:
- **Model**: Handles data and business logic (in the Models subpackage)
- **View**: Manages the visual representation (in the Views subpackage)
- **Controller**: Coordinates between Model and View (VideoGUI_Controller)

## Features
- Video display from robot cameras
- Control interface for robot movement
- Real-time updates of robot status
- Loading screen for initialization

## Usage
The main entry point for using the GUI is through the VideoGUI_Controller class:

```python
from GUI.VideoGUI_Controller import VideoGUI_Controller

# Create a controller instance
controller = VideoGUI_Controller()

# Update the view with a video frame
frame_data = get_frame_from_robot()  # Function to get frame data
controller.updateRootView(frame_data)

# Run the main GUI loop
controller.runMainLoop()
```

## Integration
The GUI package integrates with other components of the Robot Remote Control project:

- **BusTransactions**: Receives video data and sends control commands
- **Events**: Subscribes to events for real-time updates
- **SteeringInput**: Translates user input into robot control commands

## Development
The GUI is designed to be extensible:

- New views can be added to the Views subpackage
- New models can be added to the Models subpackage
- The controller can be extended to support additional functionality

## Dependencies
- Tkinter: For creating the GUI windows and widgets
- OpenCV (cv2): For processing video frames
- PIL (Python Imaging Library): For image manipulation
- ProjectLogging: For logging GUI activities