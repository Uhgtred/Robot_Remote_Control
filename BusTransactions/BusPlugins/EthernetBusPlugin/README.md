# EthernetBusPlugin Package

## Overview
The EthernetBusPlugin package provides implementations of the BusPluginInterface for Ethernet-based communication in the Robot Remote Control project. It primarily focuses on UDP socket communication, allowing the robot to send and receive messages over a network.

## Components

### Core Classes
- **UdpSocket**: Implements the BusPluginInterface for UDP socket communication. It handles setting up the socket, sending messages, and receiving messages.
- **SocketConfigs**: Contains configuration classes for socket connections, such as UdpSocketConfig.

## Features
- Secure communication with validation of sender IP address and port
- Automatic resource cleanup on program exit
- Configurable message size
- Port conflict detection to prevent multiple sockets from using the same port

## Usage
The UdpSocket class can be used directly or through the Bus class:

```python
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocket
from BusTransactions.BusPlugins.EthernetBusPlugin.SocketConfigs import UdpSocketConfig
import socket

# Create a configuration for the UDP socket
config = UdpSocketConfig(
    MyIPAddress="192.168.1.100",  # Local IP address
    YourIPAddress="192.168.1.200",  # Remote IP address
    port=5000,                     # Port number
    messageSize=1024,              # Maximum message size
    busLibrary=socket              # Socket library to use
)

# Create a UDP socket
udp_socket = UdpSocket(config)

# Send a message
udp_socket.writeBus(b"Hello, Robot!")

# Receive a message
message = udp_socket.readBus()
print(message)

# Close the socket when done
udp_socket.close()
```

## Integration with Bus
This plugin is designed to be used with the Bus class from the BusTransactions package:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocket
from BusTransactions.BusPlugins.EthernetBusPlugin.SocketConfigs import UdpSocketConfig
import socket

# Create a configuration for the UDP socket
config = UdpSocketConfig(
    MyIPAddress="192.168.1.100",
    YourIPAddress="192.168.1.200",
    port=5000,
    messageSize=1024,
    busLibrary=socket
)

# Create a UDP socket
udp_socket = UdpSocket(config)

# Create a bus with the UDP socket
bus = AbstractBus(udp_socket)

# Now you can use the bus to communicate over UDP
```
