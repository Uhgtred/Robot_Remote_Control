# BusTransactions Package

## Overview
The BusTransactions package provides a flexible framework for communication over various bus systems in the Robot Remote Control project. It implements a layered architecture that separates the concerns of bus communication, message encoding, compression, and serialization.

## Components

### Core Classes
- **Bus**: The main implementation of the BusInterface, handling communication over various bus systems.
- **BusInterface**: An abstract interface defining the contract for bus communication.
- **AbstractBus**: An abstract base class for bus implementations.

### Subpackages
- **BusPlugins**: Contains plugins for different bus systems (Ethernet, Serial, etc.)
- **Compression**: Provides protocols and implementations for data compression
- **Encoding**: Handles encoding and decoding of messages
- **Serialization**: Manages serialization and deserialization of data structures

## Usage
The Bus class is the main entry point for using this package. It can be configured with different plugins, compressors, encoders, and serializers to adapt to various communication needs.

Example:
```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import EthernetBusPlugin

# Create a bus with an Ethernet plugin
bus = AbstractBus(EthernetBusPlugin())

# Send a message
bus.writeSingleMessage("Hello, Robot!")

# Read a message
message = bus.readSingleMessage()
```

## Architecture
The package follows a layered architecture:
1. **Bus Plugins Layer**: Handles the physical communication (Ethernet, Serial, etc.)
2. **Processing Layer**: Manages compression, encoding, and serialization
3. **Interface Layer**: Provides a unified interface for the rest of the application
