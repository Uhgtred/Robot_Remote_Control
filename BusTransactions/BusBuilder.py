import atexit
import typing

import ProjectLogging
from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class BusBuilder:

    __logger = ProjectLogging.Logger('Bus', 'Bus.log').getLogger

    def __init__(self, busPlugin: BusPluginInterface) -> None:
        self.__logger: type[ProjectLogging.Logger].getLogger = ProjectLogging.Logger('BusBuilder',
                                                                     'BusBuilder.log').getLogger
        # bus needs to be set on instancing this class, since it is the only thing that is not optional.
        busPlugin: BusPluginInterface = busPlugin
        self.__logger.debug(f'BusPlugin created: {busPlugin}')
        self.busInstance = Bus(busPlugin)
        self.__logger.debug(f'Bus instance created: {self.busInstance}')

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