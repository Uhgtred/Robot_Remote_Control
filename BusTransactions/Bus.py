#!/usr/bin/env python3
# @author: Markus Kösters

import inspect

from .BusPlugins import BusPluginInterface
from .Encoding.BusEncodings import EncodingProtocol


class Bus:
    """
    Class for communication with a variety of bus-systems.
    """

    def __init__(self, bus: BusPluginInterface, encoding: EncodingProtocol):
        """
        :param bus: Bus that shall be communicated with. Needs to follow the protocol Bus.
        :param encoding: Encoding that will be used to make the messages compliant to the bus.
        """
        self.__stopFlag: bool = False
        self.encoding: EncodingProtocol = encoding
        self.bus: BusPluginInterface = bus

    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and decode a single message from the bus.
        :return: Decoded message in string format.
        """
        return self.encoding.decode(self.bus.readBus())

    def readBusUntilStopFlag(self, callbackMethod: callable, stopFlag: bool = False) -> None:
        """
        Reading messages from a bus in a loop until stopFlag is raised.
        :param callbackMethod: Method that the received messages shall be sent to.
                                Needs to accept one argument which is the message read from the bus.
        :param stopFlag: When true reading-loop stops.
        """
        self.__callBackHasInputArg(callbackMethod)
        while not stopFlag:
            callbackMethod(self.readSingleMessage())

    @staticmethod
    def __callBackHasInputArg(callbackMethod: callable) -> None:
        """
        Method that is making sure, the callback-method provided to the bus fulfills the requirements.
        :param callbackMethod: Method that will be checked for compliance.
        """
        # checking if the method is callable. Else raising an error.
        if callable(callbackMethod):
            inputArgs = inspect.signature(callbackMethod)
            # checking if the method accepts at least one argument. Else raising an error.
            if len(inputArgs.parameters) < 1:
                raise TypeError("Callback-method missing required input argument.")
        else:
            raise TypeError("Callback-method is not callable.")

    def writeSingleMessage(self, message: any) -> None:
        """
        Sending an encoded message to the bus.
        :param message: Message that will be sent to the bus.
        """
        if type(message) is not bytes:
            self.bus.writeBus(self.encoding.encode(message))
        else:
            self.bus.writeBus(message)

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
