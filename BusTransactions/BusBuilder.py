import typing


from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class BusBuilder(AbstractBus):

    def __init__(self, busPlugin: BusPluginInterface) -> None:
        # bus needs to be set on instancing this class, since it is the only thing that is not optional.
        super().__init__(busPlugin)

    def setCompressor(self, compressor: CompressionProtocol) -> typing.Self:
        # Sets the compressor-object. It is being instanced before setting it, if it has not already been instanced.
        self.__compressor: CompressionProtocol = compressor() if callable(compressor) else compressor
        return self

    def setSerializer(self, serializer: SerializationProtocol) -> typing.Self:
        self.__serializer: SerializationProtocol = serializer() if callable(serializer) else serializer
        return self

    def setEncoder(self, encoder: EncodingProtocol) -> typing.Self:
        # Sets the encoder-object. It is being instanced before setting it, if it has not already been instanced.
        self.__encoder: EncodingProtocol = encoder() if callable(encoder) else encoder
        return self

    def build(self) -> type(AbstractBus):
        return self
