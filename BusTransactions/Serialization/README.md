# Serialization Package

## Overview
The Serialization package provides a standardized interface and implementations for data serialization in the Robot Remote Control project. It is used by the BusTransactions package to convert complex data structures into a format suitable for transmission over various communication channels.

## Components

### Core Protocol
- **SerializationProtocol**: Defines the interface for serialization implementations with methods for serializing and deserializing data.

### Implementations
- **SerializerMsgPack**: Implements the SerializationProtocol using the MessagePack library, providing efficient binary serialization.

## Usage
Serialization implementations can be used directly or through the Bus class:

```python
from BusTransactions.Serialization.SerializerMsgPack import SerializerMsgPack

# Create a serializer
serializer = SerializerMsgPack()

# Serialize data
original_data = {"command": "move", "direction": "forward", "speed": 0.5}
serialized_data = serializer.serialize(original_data)

# Deserialize data
deserialized_data = serializer.deSerialize(serialized_data)

# Verify the data is the same
assert original_data == deserialized_data
```

## Integration with Bus
Serialization implementations are designed to be used with the Bus class from the BusTransactions package:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocket
from BusTransactions.Serialization.SerializerMsgPack import SerializerMsgPack

# Create a bus
bus = AbstractBus(UdpSocket(...))

# Set the serializer
bus.setSerializer(SerializerMsgPack())

# Now all data sent through the bus will be serialized using MessagePack
```

## Extending
To create a new serialization implementation, implement the SerializationProtocol:

```python
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol
import pickle  # Example using Python's pickle

class SerializerPickle(SerializationProtocol):
    def serialize(self, data: any) -> bytes:
        return pickle.dumps(data)

    def deSerialize(self, serializedData: bytes) -> any:
        return pickle.loads(serializedData)
```

## About MessagePack
MessagePack is a binary serialization format that is similar to JSON but faster and more compact. It is designed for high-performance communication and storage. The SerializerMsgPack implementation in this package uses the `msgpack` Python library to provide efficient serialization of Python objects.
