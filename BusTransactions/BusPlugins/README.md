# BusPlugins Package

## Overview
The BusPlugins package is a subpackage of BusTransactions that provides various implementations of the BusPluginInterface for different communication protocols and hardware interfaces. These plugins enable the Bus class to communicate over different physical mediums.

## Components

### Core Interface
- **BusPluginInterface**: An abstract interface that defines the contract for all bus plugins. It requires implementations to provide methods for reading from and writing to a specific bus system.

### Implementations
- **EthernetBusPlugin**: Implements communication over Ethernet networks
- **SerialBusPlugin**: Implements communication over serial interfaces (UART, RS-232, etc.)

## Usage
Bus plugins are typically instantiated and passed to a Bus object:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import EthernetBusPlugin

# Create an Ethernet bus plugin
ethernet_plugin = EthernetBusPlugin(host="192.168.1.100", port=5000)

# Create a bus with the plugin
bus = AbstractBus(ethernet_plugin)

# Now you can use the bus to communicate over Ethernet
```

## Extending
To create a new bus plugin, implement the BusPluginInterface:

```python
from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface

class MyCustomBusPlugin(BusPluginInterface):
    def readBus(self) -> bytes:
        # Implement reading from your custom bus
        ...

    def writeBus(self, message: bytes) -> None:
        # Implement writing to your custom bus
        ...
```
