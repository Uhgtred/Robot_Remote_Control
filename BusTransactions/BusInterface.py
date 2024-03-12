#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod

from .Encoding.BusEncodings import EncodingProtocol
from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface


class BusInterface(ABC):
    """
    Interface-Class for communication with a variety of bus-systems.
    """

    @abstractmethod
    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and decode a single message from the bus.
        :return: Decoded message in string format.
        """
        pass

    @abstractmethod
    def readBusUntilStopFlag(self, callbackMethod: callable, stopFlag: bool = False) -> None:
        """
        Reading messages from a bus in a loop until stopFlag is raised.
        :param callbackMethod: Method that the received messages shall be sent to.
                                Needs to accept one argument which is the message read from the bus.
        :param stopFlag: When true reading-loop stops.
        """
        pass

    @abstractmethod
    def writeSingleMessage(self, message: any) -> None:
        """
        Sending an encoded message to the bus.
        :param message: Message that will be sent to the bus.
        """
        pass

    @property
    @abstractmethod
    def stopFlag(self) -> bool:
        """
        Getter-Method for the stop-flag.
        :return: Stop-flag.
        """
        pass

    @stopFlag.setter
    @abstractmethod
    def stopFlag(self, state: bool) -> None:
        """
        Setter-method for the stop-flag.
        :param state: Stop-flag state that will be set.
        """
        pass
