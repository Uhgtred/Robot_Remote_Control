# SerialBusPlugin Package

## Overview
The SerialBusPlugin package provides implementations of the BusPluginInterface for serial communication in the Robot Remote Control project. It is designed specifically for communicating with Arduino or other microcontrollers over serial connections (UART, RS-232, etc.).

## Components

### Core Classes
- **SerialBus**: Implements the BusPluginInterface for serial communication. It handles setting up the serial connection, sending messages, and receiving messages.
- **SerialBusConfig**: Contains configuration parameters for serial connections, such as port, baud rate, and the serial library to use.

## Features
- Simple interface for serial communication
- Configurable port and baud rate
- Automatic resource cleanup on program exit
- Error handling for connection issues

## Usage
The SerialBus class can be used directly or through the Bus class:

```python
from BusTransactions.BusPlugins.SerialBusPlugin import SerialBus
from BusTransactions.BusPlugins.SerialBusPlugin import SerialBusConfig
import serial

# Create a configuration for the serial connection
config = SerialBusConfig(
    port="/dev/ttyUSB0",  # Serial port
    baudRate=9600,        # Baud rate
    busLibrary=serial.Serial  # Serial library to use
)

# Create a serial bus
serial_bus = SerialBus(config)

# Send a message
serial_bus.writeBus(b"Hello, Arduino!")

# Receive a message
message = serial_bus.readBus()
print(message)

# Close the connection when done
serial_bus.close()
```

## Integration with Bus
This plugin is designed to be used with the Bus class from the BusTransactions package:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.SerialBusPlugin import SerialBus
from BusTransactions.BusPlugins.SerialBusPlugin import SerialBusConfig
import serial

# Create a configuration for the serial connection
config = SerialBusConfig(
    port="/dev/ttyUSB0",
    baudRate=9600,
    busLibrary=serial.Serial
)

# Create a serial bus
serial_bus = SerialBus(config)

# Create a bus with the serial bus
bus = AbstractBus(serial_bus)

# Now you can use the bus to communicate over serial
```

## Hardware Compatibility
This plugin is primarily designed for communication with Arduino boards, but it can be used with any device that supports serial communication, such as:
- Arduino (Uno, Mega, Nano, etc.)
- Raspberry Pi (via GPIO UART)
- Other microcontrollers with serial interfaces
- USB-to-Serial adapters
