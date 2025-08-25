#!/usr/bin/env python3
# @author      Markus Kösters

import serial

import ProjectLogging
from .SerialBusConfig import SerialBusConfig
from ..BusPluginInterface import BusPluginInterface


class SerialBus(BusPluginInterface):
    """
    Class for handling a serial-connection to an Arduino. And reading/writing messages to it.
    """

    def __init__(self, config: SerialBusConfig):
        self.__logger: type[ProjectLogging.Logger].getLogger = ProjectLogging.Logger('SerialBus',
                                                                                     'SerialBus.log').getLogger
        self.serialBus: serial.Serial | None = None
        self.__port = None
        self.__baudRate = None
        self.setConfig(config)

    def readBus(self) -> bytes:
        """
        Method for reading from the serial-bus.
        :return: Bytes containing the message.
        """
        return self.serialBus.read()

    def writeBus(self, message: bytes) -> None:
        """
        Method for writing to the serial-bus.
        :param message: Message that shall be sent to the bus.
        """
        self.serialBus.write(message)

    def _setupSerialBus(self, serialBus: serial.Serial) -> serial.Serial:
        """
        Initializing the microcontroller bus-settings.
        """
        serialBus.baudrate = self.__baudRate  # baudrate is of type int
        serialBus.port = self.__port  # port is of type str
        if not serialBus.is_open:
            serialBus.open()
        return serialBus

    def setConfig(self, config: SerialBusConfig) -> None:
        """
        Setter-method for the config.
        :param config: Dictionary containing the information about the bus.
        """
        # check if the busLibrary-object has already been instanced
        bus: serial.Serial = config.busLibrary() if callable(config.busLibrary) else config.busLibrary
        self.__port: str = config.port
        self.__baudRate: int = config.baudRate
        self.serialBus: serial.Serial = self._setupSerialBus(bus)

    def closeBus(self) -> None:
        try:
            self.__logger.info(f"Serialbus [{self.serialBus}] is being closed!")
            self.serialBus.close()
        except Exception as exception:
            self.__logger.warning(f"Serialbus [{self.serialBus}] could not be closed properly! "
                                  f"Original Error-message: {exception}")