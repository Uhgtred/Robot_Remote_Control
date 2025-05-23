#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod

import ProjectLogging


class BusPluginInterface(ABC):
    """
    Interface for the BusPlugins used by the Bus-class.
    """
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('BusPluginInterface',
                                                                      'BusPluginInterface.log').getLogger

    @abstractmethod
    def readBus(self) -> bytes:
        """
        Interface-method for reading from a bus.
        :return: Bytes containing the message.
        """
        ...

    @abstractmethod
    def writeBus(self, message: bytes) -> None:
        """
        Interface-method for writing to a bus.
        :param message: Message that shall be sent to the bus.
        """
        ...

