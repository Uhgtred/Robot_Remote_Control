# Todo: implement this
import typing

from BusTransactions.BusInterface import BusInterface
from BusTransactions.Compression.CompressorInterface import CompressorInterface
from BusTransactions.Encoding import EncodingProtocol


class BusBuilder:

    def __init__(self, bus: BusInterface):
        self.bus: BusInterface = bus()

    def setCompressor(self, compressor: CompressorInterface) -> typing.Self:
        self.bus.setCompressor(compressor)
        return self

    def setSerializer(self, serializer: SerializerInterface) -> typing.Self:
        self.bus.setSerializer(serializer)
        return self

    def setEncoder(self, encoder: EncodingProtocol) -> typing.Self:
        self.bus.setEncoder(encoder)
        return self

    def build(self):
        return self.bus
