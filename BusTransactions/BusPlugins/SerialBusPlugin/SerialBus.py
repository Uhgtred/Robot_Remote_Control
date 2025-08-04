#!/usr/bin/env python3
# @author      Markus Kösters

import atexit
import serial

from .SerialBusConfig import SerialBusConfig
from ..BusPluginInterface import BusPluginInterface


class SerialBus(BusPluginInterface):
    """
    Class for handling a serial-connection to an Arduino. And reading/writing messages to it.
    """

    def __init__(self, config: SerialBusConfig):
        self.bus = None
        self.__port = None
        self.__baudRate = None
        self.setConfig(config)

    def readBus(self) -> bytes:
        """
        Method for reading from the serial-bus.
        :return: Bytes containing the message.
        """
        return self.bus.read()

    def writeBus(self, message: bytes) -> None:
        """
        Method for writing to the serial-bus.
        :param message: Message that shall be sent to the bus.
        """
        self.bus.write(message)

    def _setupBus(self, bus: type(serial.Serial)) -> type(serial.Serial):
        """
        Initializing the microcontroller bus-settings.
        """
        bus.baudrate = self.__baudRate  # baudrate is of type int
        bus.port = self.__port  # port is of type str
        if not bus.is_open:
            bus.open()
        return bus

    def setConfig(self, config: SerialBusConfig) -> None:
        """
        Setter-method for the config.
        :param config: Dictionary containing the information about the bus.
        """
        # check if the busLibrary-object has already been instanced
        bus: type(serial.Serial) = config.busLibrary() if callable(config.busLibrary) else config.busLibrary
        self.__port: str = config.port
        self.__baudRate: int = config.baudRate
        self.bus: type(serial.Serial) = self._setupBus(bus)

    def close(self) -> None:
        try:
            self.__logger.info(f"Serialbus [{self.bus}] is being closed!")
            self.bus.close()
        except Exception as exception:
            self.__logger.warning(f"Serialbus [{self.bus}] could not be closed properly! "
                                  f"Original Error-message: {exception}")