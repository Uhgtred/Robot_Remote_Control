# Events Package

## Overview
The Events package provides an event-driven architecture for the Robot Remote Control project. It implements a publish-subscribe pattern that allows different components of the system to communicate with each other without direct dependencies.

## Components

### Core Classes
- **AbstractEvent**: An abstract base class that implements the event subscription and notification mechanism. It allows methods to subscribe to events and receive notifications when those events occur.
- **EventManager**: A class that manages events, allowing for event creation, subscription, and retrieval. It maintains a dictionary of events and provides methods for interacting with them.

## Features
- Decoupled communication between components
- Support for multiple subscribers per event
- Verbose notification mode for detailed logging
- Centralized event management

## Usage

### Creating and Managing Events
```python
from Events.EventManager import EventManager

# Create an event manager
event_manager = EventManager()

# Create a new event
motion_event = event_manager.produceConcreteEvent("motion_detected")

# Get a list of all events
events = event_manager.getEventsList
print(f"Available events: {events}")
```

### Subscribing to Events
```python
from Events.EventManager import EventManager

# Create an event manager
event_manager = EventManager()

# Define a callback function
def handle_motion(data):
    print(f"Motion detected: {data}")

# Subscribe to an event
event_manager.subscribeToEvent("motion_detected", handle_motion)
```

### Notifying Subscribers
```python
from Events.EventManager import EventManager

# Create an event manager
event_manager = EventManager()

# Get an existing event
motion_event = event_manager.produceConcreteEvent("motion_detected")

# Notify subscribers
motion_event.notifySubscribers({"location": "living_room", "intensity": 0.8})

# Notify subscribers with verbose logging
motion_event.notifySubscriberVerbose({"location": "kitchen", "intensity": 0.5})
```

## Integration
The Events package is designed to be used throughout the Robot Remote Control project to facilitate communication between different components:

- **BusTransactions**: Notify when messages are received or sent
- **GUI**: Update the user interface when robot state changes
- **SteeringInput**: Broadcast control commands to the robot
- **Runners**: Signal when processes start or complete

## Architecture
The package follows a simple architecture:
1. **Event Creation**: Events are created and managed by the EventManager
2. **Subscription**: Components subscribe to events they are interested in
3. **Notification**: When an event occurs, all subscribers are notified with the relevant data