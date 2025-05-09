import typing

from BusTransactions.BusInterface import BusInterface
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class BusBuilder:

    def __init__(self, bus: type(BusInterface)) -> None:
        # bus needs to be set on instancing this class, since it is the only thing that is not optional.
        self.bus: BusInterface = bus()

    def setCompressor(self, compressor: CompressionProtocol) -> typing.Self:
        self.bus.setCompressor(compressor)
        return self

    def setSerializer(self, serializer: SerializationProtocol) -> typing.Self:
        self.bus.setSerializer(serializer)
        return self

    def setEncoder(self, encoder: EncodingProtocol) -> typing.Self:
        self.bus.setEncoder(encoder)
        return self

    def build(self) -> type(BusInterface):
        return self.bus
