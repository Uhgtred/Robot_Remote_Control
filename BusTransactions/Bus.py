#!/usr/bin/env python3
# @author: Markus Kösters

import inspect
import threading

import ProjectLogging
from .BusInterface import BusInterface
from .BusPlugins import BusPluginInterface
from .Compression.CompressorInterface import CompressorInterface
from .Encoding.BusEncodings import EncodingProtocol
from .Serialization.SerializerInterface import SerializerInterface


class Bus(BusInterface):
    """
    Class for communication with a variety of bus-systems.
    """

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Bus', 'Bus.log').getLogger

    def __init__(self, bus: BusPluginInterface):
        """
        :param bus: Bus that will be communicated with. Needs to follow the protocol Bus.
        :param bus: Bus that shall be communicated with. Needs to follow the protocol Bus.
        """
        self.__stopFlag: bool = False
        self.bus: BusPluginInterface = bus
        self.__compressor: CompressorInterface | None = None
        self.__serializer: SerializerInterface | None = None
        self.__encoder: EncodingProtocol | None = None

    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and decode a single message from the bus.
        :return: Decoded message in string format.
        """
        self.__logger.debug(f'Reading message from bus: {self.bus.__class__.__name__}')
        try:
            message: bytes = self.bus.readBus()
        except Exception as exception:
            self.__logger.debug(f'Error while trying to read a message from the bus: {exception}')
            raise BaseException(f'Error while trying to read a message from the bus: {exception}')
        message: bytes = self.__deCompress(message)
        message: bytes = self.__deSerialize(message)
        message: any = self.__decode(message)
        self.__logger.debug(f'Message that has been received: {message}')
        return message

    def readBusUntilStopFlag(self, callbackMethod: callable, *args, **kwargs) -> None:
        """
        Reading messages from a bus in a loop until stopFlag is raised.
        :param callbackMethod: Method that the received messages shall be sent to.
                                Needs to accept one argument which is the message read from the bus.
        """
        self.__callBackHasInputArg(callbackMethod)
        thread = threading.Thread(target=self.__readLoop, args=(callbackMethod, *args), kwargs=kwargs)
        thread.start()

    def __readLoop(self, callbackMethod: callable, *args, **kwargs) -> None:
        """
        Method that includes the logic to read a message from the bus in a loop until stopFlag is raised.
        :param callbackMethod: Method that the received messages will be sent to.
        :param args: Further positional arguments to the callback method.
        :param kwargs: Further keyword arguments to the callback method.
        """
        while not self.__stopFlag:
            try:
                self.__logger.debug(f'Trying to read a message with callback-method {self.readSingleMessage.__name__}\n'
                                    f'\twith args: {args}\n'
                                    f'\tand kwargs: {kwargs}'
                                    f'\ton bus: {self.bus.__class__.__name__}')
                message: any = self.readSingleMessage()
                self.__logger.debug(f'Message received: {message}')
                callbackMethod(message, *args, **kwargs)
            except Exception as e:
                self.__logger.error(f'Error while reading message: {e}')


    @staticmethod
    def __callBackHasInputArg(callbackMethod: callable) -> None:
        """
        Method that is making sure, the callback-method provided to the bus fulfills the requirements.
        :param callbackMethod: Method that will be checked for compliance.
        """
        # Checking if the method is callable. Else raising an error.
        if callable(callbackMethod):
            inputArgs = inspect.signature(callbackMethod)
            # Checking if the method accepts at least one argument. Else raising an error.
            if len(inputArgs.parameters) < 1:
                raise TypeError("Callback-method missing required input argument.")
        else:
            raise TypeError("Callback-method is not callable.")

    def writeSingleMessage(self, message: any) -> None:
        """
        Sending an encoded message to the bus.
        :param message: Message that will be sent to the bus.
        """
        self.__logger.debug(f'Sending message: {message} to bus: {self.bus.__class__.__name__}')
        message: bytes = self.__encode(message)
        message: bytes = self.__serialize(message)
        message: bytes = self.__compress(message)
        try:
            self.bus.writeBus(message)
        except Exception as exception:
            self.__logger.debug(f'Error while trying to send a message to the bus: {exception}!')
            raise BaseException(f'Error while trying to send a message to the bus: {exception}!')

    @property
    def stopFlag(self) -> bool:
        """
        Getter-Method for the stop-flag.
        :return: Stop-flag.
        """
        return self.__stopFlag

    @stopFlag.setter
    def stopFlag(self, state: bool) -> None:
        """
        Setter-method for the stop-flag.
        :param state: Stop-flag state that will be set.
        """
        self.__stopFlag = state

    def setCompressor(self, compressor: CompressorInterface) -> None:
        self.__compressor: CompressorInterface = compressor

    def __compress(self, data: bytes) -> bytes:
        """
        Method for compressing data before sending it via bus-object.
        :param data:
        :return:
        """
        return self.__compressor.compress(data) if self.__compressor else data

    def __deCompress(self, data: bytes) -> bytes:
        return self.__compressor.deCompress(data) if self.__compressor else data

    def setEncoder(self, encoder: EncodingProtocol) -> None:
        self.__encoder: EncodingProtocol = encoder

    def __encode(self, data: any) -> bytes:
        return self.__encoder.encode(data) if self.__encoder else data

    def __decode(self, data: bytes) -> any:
        return self.__encoder.decode(data) if self.__encoder else data

    def setSerializer(self, serializer: SerializerInterface) -> None:
        self.__serializer: SerializerInterface = serializer

    def __serialize(self, data: any) -> bytes:
        return self.__serializer.serialize(data) if self.__serializer else data

    def __deSerialize(self, data: bytes) -> any:
        return self.__serializer.deSerialize(data) if self.__serializer else data
