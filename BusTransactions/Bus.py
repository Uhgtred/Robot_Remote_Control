#!/usr/bin/env python3
# @author: Markus Kösters

import inspect
import threading

import ProjectLogging
from .BusPlugins import BusPluginInterface
from .Encoding.BusEncodings import EncodingProtocol
from .BusInterface import BusInterface


class Bus(BusInterface):
    """
    Class for communication with a variety of bus-systems.
    """

    def __init__(self, bus: BusPluginInterface, encoding: EncodingProtocol):
        """
        :param bus: Bus that will be communicated with. Needs to follow the protocol Bus.
        :param bus: Bus that shall be communicated with. Needs to follow the protocol Bus.
        :param encoding: Encoding that will be used to make the messages compliant to the bus.
        """
        self.__stopFlag: bool = False
        self.encoding: EncodingProtocol = encoding
        self.bus: BusPluginInterface = bus
        self.__logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Bus', 'Bus.log').getLogger

    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and decode a single message from the bus.
        :return: Decoded message in string format.
        """
        message: any = self.encoding.decode(self.bus.readBus())
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
                callbackMethod(self.readSingleMessage(), *args, **kwargs)
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

    def writeSingleMessage(self, message: any, verbose: bool = False) -> None:
        """
        Sending an encoded message to the bus.
        :param verbose: Makes the method return command-line output.
        :param message: Message that will be sent to the bus.
        """
        if verbose:
            self.__logger.debug(f'Sending message: {message} to bus: {self.bus.__class__.__name__}')
        self.bus.writeBus(self.encoding.encode(message))

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
