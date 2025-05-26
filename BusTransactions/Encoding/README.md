# Encoding Package

## Overview
The Encoding package provides a standardized interface and implementations for data encoding in the Robot Remote Control project. It is used by the BusTransactions package to encode data before transmission and decode data after reception, ensuring proper data format for different communication channels.

## Components

### Core Protocol
- **EncodingProtocol**: Defines the interface for encoding implementations with static methods for encoding and decoding messages.

### Implementations
- **ArduinoSerialEncoder**: Encoder for communication with Arduino over serial connections
- **ImageDataEncoder**: Specialized encoder for image data
- **PythonEncoder**: General-purpose encoder for Python objects
- **SocketEncoderJson**: JSON-based encoder for socket communications

### Factory
- **EncodingFactory**: Factory class for creating encoder instances based on configuration or requirements

## Usage
Encoding implementations can be used directly or through the Bus class:

```python
from BusTransactions.Encoding.SocketEncoderJson import SocketEncoderJson

# Encode data
original_data = {"command": "move", "direction": "forward", "speed": 0.5}
encoded_data = SocketEncoderJson.encode(original_data)

# Decode data
decoded_data = SocketEncoderJson.decode(encoded_data)

# Verify the data is the same
assert original_data == decoded_data
```

## Integration with Bus
Encoding implementations are designed to be used with the Bus class from the BusTransactions package:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocket
from BusTransactions.Encoding.SocketEncoderJson import SocketEncoderJson

# Create a bus
bus = AbstractBus(UdpSocket(...))

# Set the encoder
bus.setEncoder(SocketEncoderJson)

# Now all data sent through the bus will be encoded using JSON
```

## Extending
To create a new encoding implementation, implement the EncodingProtocol:

```python
from BusTransactions.Encoding.EncodingProtocol import EncodingProtocol
import msgpack  # Example using MessagePack

class MessagePackEncoder(EncodingProtocol):
    @staticmethod
    def encode(message: any) -> bytes:
        return msgpack.packb(message)

    @staticmethod
    def decode(message: bytes) -> any:
        return msgpack.unpackb(message)
```

## Choosing an Encoder
- **ArduinoSerialEncoder**: Use for communication with Arduino devices
- **ImageDataEncoder**: Use for transmitting image data efficiently
- **PythonEncoder**: Use for general Python objects when both ends are Python
- **SocketEncoderJson**: Use for human-readable JSON data over network connections
