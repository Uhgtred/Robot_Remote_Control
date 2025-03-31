#!/usr/bin/env python3
# @author: Markus Kösters
import logging

from .EthernetBusPlugin import UdpSocket, SocketConfigs
from .EthernetBusPlugin.test_UnitTests import MockSocket
from .SerialBusPlugin import SerialBus, SerialBusConfig
from .SerialBusPlugin.UnitTests.SerialBusMock import MockSerialBus


class BusPluginFactory:
    """
    Factory class for creating various communication plugins.

    The BusPluginFactory class provides several static methods to produce instances of different
    communication protocol plugins, including SerialBus, UDP socket, and their respective stub
    versions. These plugins are configured with appropriate settings predefined in the factory
    methods, allowing easy initialization of communication interfaces.

    :ivar default_device_path: Default device path for serial communication.
    :type default_device_path: str
    :ivar default_baud_rate: Default baud rate for serial communication.
    :type default_baud_rate: int
    """

    __logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def produceSerialBusArduinoPlugin() -> SerialBus:
        """
        Method for creating an instance of a SerialBus.
        :return: SerialBus-instance.
        """
        config = SerialBusConfig('/dev/ttyACM0', 115200)
        return SerialBus(config)

    @staticmethod
    def produceSerialBusStubPlugin() -> SerialBus:
        """
        Generates and returns a SerialBus instance configured with a mock serial bus.

        This static method initializes a SerialBusConfig object with default settings
        including the device path, baud rate, and a mocked serial bus class. It then
        uses this configuration to create and return a new SerialBus instance.

        :raises ValueError: Raised if the provided configuration values are invalid.

        :return: An instance of SerialBus configured using default parameters for
                 mocking a serial bus communication.
        :rtype: SerialBus
        """
        config: SerialBusConfig = SerialBusConfig('/dev/ttyACM0', 115200, MockSerialBus)

        return SerialBus(config)

    @staticmethod
    def produceUdpSocketPlugin(port: int) -> UdpSocket:
        """
        This static method initializes and produces an instance of the UdpSocket plugin
        using the provided port number and optional message size. The method acts as a
        factory for creating and returning a configured UdpSocket object.

        :param port: The port number to bind the UDP socket to.
        :type port: Int

        :return: An instance of `Tcp_Udp_sockets.UdpSocket` configured with the
            specified port and message size.
        :rtype: UdpSocket.UdpSocket
        """
        config: SocketConfigs = SocketConfigs.UdpSocketConfig(port=port)
        return UdpSocket(config)

    @staticmethod
    def produceUdpStubPlugin(port: int) -> UdpSocket:
        """
        Produces an UDP stub plugin for mock testing or emulation. This method creates a UDP
        socket configuration and initializes an UDP socket instance using a mock socket library.

        :param port: The port number to initialize the UDP socket configuration.
        :type port: Int
        :return: An instance of UdpSocket configured with the specified port and using
                 the mock socket library.
        :rtype: UdpSocket
        """
        config: SocketConfigs = SocketConfigs.UdpSocketConfig(port=port, busLibrary=MockSocket)
        return UdpSocket(config)
