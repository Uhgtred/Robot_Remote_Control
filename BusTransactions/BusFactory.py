#!/usr/bin/env python3
# @author: Markus Kösters

from .Bus import Bus
from .BusPlugins import BusPluginInterface
from .BusPlugins import BusPluginFactory
from .Encoding import EncodingFactory
from .Encoding.BusEncodings import EncodingProtocol


class BusFactory:
    """
    Provides a factory for creating instances of bus-transceivers with different configurations.

    This class contains static methods to produce various types of bus-transceivers, including
    serial transceivers and UDP-based transceivers with optional stubbing capabilities. Clients
    can specify the appropriate configurations required for communication, such as encoding
    protocols and network ports.

    Methods in this factory integrate bus plugins with encoding protocols to form complete bus
    systems, ensuring compatibility for communication processes.

    :ivar attribute1: Description of attribute1.
    :type attribute1: type
    :ivar attribute2: Description of attribute2.
    :type attribute2: type
    """

    @staticmethod
    def produceCustomBusTransceiver(bus: BusPluginInterface, encoding: EncodingProtocol) -> Bus:
        """
        Method for producing an instance of a bus-transceiver.
        :param bus: Bus-Class that will be communicated with, produced by Factory-class in BusPlugins-Module.
        :param encoding: Encoding that decides the format of the messages.
        """
        # check if encoding has already been instanced
        encoding: EncodingProtocol = encoding() if callable(encoding) else encoding
        transceiver = Bus(bus, encoding)
        return transceiver

    @staticmethod
    def produceSerialTransceiver() -> Bus:
        """
        Produces a serial transceiver configured with Arduino's serial bus plugin and
        related encoding protocol. Combines the plugin and encoding configuration into a
        Bus instance for communication compatibility.

        :rtype: Bus
        :return: The configured serial transceiver bus object.
        """
        encoding: EncodingProtocol = EncodingFactory.arduinoSerialEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceSerialBusArduinoPlugin()
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_Transceiver(port: int) -> Bus:
        """
        Produces a UDP transceiver bus object configured with the specified port and
        encoding protocol. Depending on whether the stub parameter is set to True, either
        a stub plugin or a socket plugin will be used for the created transceiver. This
        method integrates the generated bus plugin with the defined encoding protocol.

        :param port: Network port number where the transceiver will operate.
        :type port: int
        :return: Configured Bus object equipped with a UDP transceiver.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.socketEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(port=port)
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_TransceiverWithStub(port: int) -> Bus:
        """
        Creates and configures a UDP-based transceiver stub with the specified port.

        This static method initializes a bus communication system configured with
        UDP stubbing behavior. It sets up an encoding protocol and utilizes a UDP
        stub plugin, allowing for a specific port to be assigned for communication.
        The method combines these components into a `Bus` instance which can be
        used for further communication processes.

        :param port: The port number to be used for creating the UDP stub.
        :type port: int
        :return: A fully configured `Bus` instance with UDP-based stub communication.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.socketEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(port=port)
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
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(port=port)
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_ImageDataReceiverWithStub(port: int) -> Bus:
        """
        Produces a UDP image data receiver using a stub plugin and appropriate encoding.
        The method sets up an encoding protocol for image receiving and creates a BusPluginInterface
        using a UDP stub plugin for the specified port. It combines these configurations into
        a Bus instance and returns it.

        :param port: The port number on which the UDP stub plugin will operate.
        :type port: int

        :return: A configured Bus instance capable of receiving image data via UDP.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.produceImageReceiverEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(port=port)
        return Bus(busPlugin, encoding)
