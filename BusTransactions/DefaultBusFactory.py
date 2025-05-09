#!/usr/bin/env python3
# @author: Markus Kösters

from .Bus import Bus
from .BusBuilder import BusBuilder
from .BusInterface import BusInterface
from .BusPlugins import BusPluginInterface
from .BusPlugins import BusPluginFactory
from .Compression.CompressorZlib import CompressorZlib
from .Encoding import EncodingFactory
from .Encoding.EncodingProtocol import EncodingProtocol
from .Serialization.SerializerMsgPack import SerializerMsgPack


class DefaultBusFactory:
    """
    Factory for creating an instance of a bus-transceiver utilizing the BusBuilder.
    """

    @staticmethod
    def produceSerialTransceiver() -> BusInterface:
        """
        Creates and configures a serial transceiver for Arduino communication. This involves
        initializing an encoding protocol and setting up a bus plugin specific to Arduino,
        and then using these components to produce and return a configured `Bus` object.

        :staticmethod:

        :return: An instance of `Bus` configured with the Arduino-specific serial bus plugin
                 and encoding protocol.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.arduinoSerialEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceSerialBusArduinoPlugin()
        bus: BusInterface = (BusBuilder(busPlugin)
                             .setEncoder(encoding)
                             .build())
        return bus

    @staticmethod
    def produceSerialTransceiverWithStub() -> BusInterface:
        """
        Produces a serial transceiver with a stub implementation using the Arduino serial
        encoding protocol. This function sets up a mock serial bus plugin and prepares
        it with the required encoding to simulate serial communication.

        :rtype: Bus
        :return: Returns an instance of the Bus class initialized with a stub serial
                 bus plugin and Arduino serial encoding protocol.
        """
        encoding: EncodingProtocol = EncodingFactory.arduinoSerialEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceSerialBusStubPlugin()
        bus: BusInterface = (BusBuilder(busPlugin)
                             .setEncoder(encoding)
                             .build())
        return bus

    @staticmethod
    def produceUDP_Transceiver(port: int) -> BusInterface:
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
        bus: BusInterface = (BusBuilder(busPlugin)
                             .setEncoder(encoding)
                             .build())
        return bus

    @staticmethod
    def produceUDP_TransceiverWithStub(port: int) -> BusInterface:
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
        bus: BusInterface = (BusBuilder(busPlugin)
                             .setEncoder(encoding)
                             .build())
        return bus


    @staticmethod
    def produceUDP_ImageDataTransceiver(port: int) -> BusInterface:
        """
        Creates an UDP-based Image Data Receiver with options for using a stub plugin or
        a real socket plugin, and returns a configured Bus instance which includes the
        desired encoding protocol and the chosen bus plugin.

        :param port: Specifies the UDP port number on which the receiver will operate.
        :type port: int
        :return: An instance of Bus configured with the chosen UDP plugin and encoding protocol.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.produceImageDataEncoder()
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(port=port)
        bus: BusInterface = (BusBuilder(busPlugin)
                             .setSerializer(SerializerMsgPack())
                             .setEncoder(encoding)
                             .setCompressor(CompressorZlib)
                             .build())
        return bus

    @staticmethod
    def produceUDP_ImageDataTransceiverWithStub(port: int) -> BusInterface:
        """
        Produces an instance of a UDP Image Data Receiver with a stub implementation.

        This static method configures and initializes a Bus object capable of
        receiving image data over UDP using a specific stub plugin. The method
        utilizes factory classes to provide the necessary encoding protocol and
        plugin implementation.

        :param port: The UDP port number on which the receiver should listen.
        :type port: int

        :return: An instance of the initialized Bus configured with the appropriate
            encoding protocol and stub plugin.
        :rtype: Bus
        """
        encoding: EncodingProtocol = EncodingFactory.produceImageDataEncoder()
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(port=port)
        bus: BusInterface = (BusBuilder(bus=busPlugin)
                             .setSerializer(SerializerMsgPack())
                             .setCompressor(CompressorZlib())
                             .setEncoder(encoding)
                             .build())
        return bus
