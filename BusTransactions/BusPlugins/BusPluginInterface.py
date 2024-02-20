#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class BusPluginInterface(ABC):

    @abstractmethod
    def readBus(self) -> bytes:
        """
        Interface-method for reading from a bus.
        :return: Bytes containing the message.
        """
        pass

    @abstractmethod
    def writeBus(self, message: bytes) -> None:
        """
        Interface-method for writing to a bus.
        :param message: Message that shall be sent to the bus.
        """
        pass
