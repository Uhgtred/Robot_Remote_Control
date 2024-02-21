#!/usr/bin/env python3
# @author: Markus Kösters

from . import BusInterface
from .Bus import Bus
from .BusPlugins import BusPluginFactory
from .Encoding import EncodingFactory


class BusFactory:
    """
    Factory for creating an instance of a bus-transceiver.
    """

    @staticmethod
    def produceBusTransceiver(bus: type(BusPluginFactory), encoding: type(EncodingFactory)) -> Bus:
        """
        Method for producing an instance of a bus-transceiver.
        :param bus: Bus-Class that will be communicated with, produced by Factory-class in BusPlugins-Module.
        :param encoding: Encoding that decides the format of the messages.
        """
        # check if encoding has already been instanced
        if callable(encoding):
            encoding = encoding()
        transceiver = Bus(bus, encoding)
        return transceiver

    @classmethod
    def produceSerialTransceiver(cls) -> Bus:
        """
        Method for creating an instance of a serial-bus transceiver that connects to arduino.
        """
        encoding = EncodingFactory.arduinoSerialEncoding
        busPlugin = BusPluginFactory.produceSerialBusArduinoPlugin()
        return cls.produceBusTransceiver(busPlugin, encoding)

    @classmethod
    def produceUDP_Transceiver(cls) -> Bus:
        """
        Method for creating an instance of an udp-socket.
        :return:
        """
        encoding = EncodingFactory.socketEncoding()
        busPlugin = BusPluginFactory.produceUdpSocketPlugin()  # Todo: make check if some socket is already running on that port, could be the wrong location for that here!
        return cls.produceBusTransceiver(busPlugin, encoding)
