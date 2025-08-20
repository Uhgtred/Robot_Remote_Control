import atexit
import typing

from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class BusBuilder:

    def __init__(self, busPlugin: BusPluginInterface) -> None:
        # bus needs to be set on instancing this class, since it is the only thing that is not optional.
        busPlugin: BusPluginInterface = busPlugin
        self.busInstance = Bus(busPlugin)

    def setCompressor(self, compressor: CompressionProtocol | type[CompressionProtocol]) -> typing.Self:
        # Sets the compressor-object. It is being instanced before setting it, if it has not already been instanced.
        self.busInstance._compressor = compressor() if callable(compressor) else compressor
        return self

    def setSerializer(self, serializer: SerializationProtocol | type[SerializationProtocol]) -> typing.Self:
        self.busInstance._serializer = serializer() if callable(serializer) else serializer
        return self

    def setEncoder(self, encoder: EncodingProtocol | type[EncodingProtocol]) -> typing.Self:
        # Sets the encoder-object. It is being instanced before setting it, if it has not already been instanced.
        self.busInstance._encoder = encoder() if callable(encoder) else encoder
        return self

    def build(self) -> AbstractBus:
        return self.busInstance


class Bus(AbstractBus):

    def __init__(self, busPlugin: BusPluginInterface) -> None:
        super().__init__(busPlugin)