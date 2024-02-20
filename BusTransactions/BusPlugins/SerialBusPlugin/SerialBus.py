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
        # Making sure the bus is closed when instance dies.
        atexit.register(self.bus.close)

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

    def _setupBus(self, bus: serial.Serial) -> object:
        """
        Initializing the microcontroller bus-settings.
        """
        bus.baudrate = self.__baudRate
        bus.port = self.__port
        if not bus.is_open:
            bus.open()
        return bus

    def setConfig(self, config: SerialBusConfig) -> None:
        """
        Setter-method for the config.
        :param config: Dictionary containing the information about the bus.
        """
        # check if the busLibrary-object has already been instanced
        if callable(config.busLibrary):
            bus = config.busLibrary()
        else:
            bus = config.busLibrary
        self.__port = config.port
        self.__baudRate = config.baudRate
        self.bus: serial.Serial = self._setupBus(bus)
