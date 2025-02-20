#!/usr/bin/env python3
# @author: Markus Kösters

from .Bus import Bus
from .BusPlugins import BusPluginInterface
from .BusPlugins import BusPluginFactory
from .Encoding import EncodingFactory
from .Encoding.BusEncodings import EncodingProtocol


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
            encoding: EncodingProtocol = encoding()
        transceiver = Bus(bus, encoding)
        return transceiver

    @staticmethod
    def produceSerialTransceiver() -> Bus:
        """
        Method for creating an instance of a serial-bus transceiver that connects to arduino.
        """
        encoding: EncodingProtocol = EncodingFactory.arduinoSerialEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceSerialBusArduinoPlugin()
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_Transceiver(port: int, stub: bool = False) -> Bus:
        """
        Produces a UDP transceiver bus object configured with the specified port and
        encoding protocol. Depending on whether the stub parameter is set to True, either
        a stub plugin or a socket plugin will be used for the created transceiver. This
        method integrates the generated bus plugin with the defined encoding protocol.

        :param port: Network port number where the transceiver will operate.
        :type port: int
        :param stub: Boolean flag to determine whether to use a UDP stub plugin
                     (True) or a UDP socket plugin (False). Default is False.
        :type stub: bool
        :return: Configured Bus object equipped with a UDP transceiver.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.socketEncoding()
        if stub:
            busPlugin: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(port=port)
        else:
            busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(port=port)
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_ImageDataReceiver(port: int, stub: bool = False) -> Bus:
        """
        Creates an UDP-based Image Data Receiver with options for using a stub plugin or
        a real socket plugin, and returns a configured Bus instance which includes the
        desired encoding protocol and the chosen bus plugin.

        :param port: Specifies the UDP port number on which the receiver will operate.
        :type port: int
        :param stub: Determines whether to use a stub plugin (for testing) or a real socket plugin. Defaults to False.
        :type stub: bool
        :return: An instance of Bus configured with the chosen UDP plugin and encoding protocol.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.produceImageReceiverEncoding()
        if stub:
            busPlugin: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(port=port)
        else:
            busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(port=port)
        return Bus(busPlugin, encoding)
