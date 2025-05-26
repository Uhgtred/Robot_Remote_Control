# Compression Package

## Overview
The Compression package provides a standardized interface and implementations for data compression in the Robot Remote Control project. It is used by the BusTransactions package to compress data before transmission and decompress data after reception, improving bandwidth efficiency.

## Components

### Core Protocol
- **CompressionProtocol**: Defines the interface for compression implementations with methods for compressing and decompressing data.

### Implementations
- **CompressorZlib**: Implements the CompressionProtocol using the zlib library, providing efficient data compression.

## Usage
Compression implementations can be used directly or through the Bus class:

```python
from BusTransactions.Compression.CompressorZlib import CompressorZlib

# Create a compressor
compressor = CompressorZlib()

# Compress data
original_data = b"Hello, Robot!"
compressed_data = compressor.compress(original_data)

# Decompress data
decompressed_data = compressor.deCompress(compressed_data)

# Verify the data is the same
assert original_data == decompressed_data
```

## Integration with Bus
Compression implementations are designed to be used with the Bus class from the BusTransactions package:

```python
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocket
from BusTransactions.Compression.CompressorZlib import CompressorZlib

# Create a bus
bus = AbstractBus(UdpSocket(...))

# Set the compressor
bus.setCompressor(CompressorZlib())

# Now all data sent through the bus will be compressed using zlib
```

## Extending
To create a new compression implementation, implement the CompressionProtocol:

```python
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
import bz2  # Example using bz2 compression

class CompressorBzip2(CompressionProtocol):
    def compress(self, data: bytes) -> bytes:
        return bz2.compress(data)

    def deCompress(self, compressedData: bytes) -> bytes:
        return bz2.decompress(compressedData)
```
