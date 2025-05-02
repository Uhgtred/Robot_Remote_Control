from typing import Self

from BusTransactions.BusInterface import BusInterface
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol

"""
Todo: get implementation done.
"""

class BusBuilder:

    def __init__(self, bus: type(BusInterface)) -> None:
        self.bus: BusInterface = bus()

    def setCompressor(self, compressor: CompressionProtocol) -> Self:
        self.bus.setCompressor(compressor)
        return self

    def setSerializer(self, serializer: SerializationProtocol) -> Self:
        self.bus.setSerializer(serializer)
        return self

    def setEncoder(self, encoder: EncodingProtocol) -> Self:
        self.bus.setEncoder(encoder)
        return self

    def build(self):
        return self.bus
