#!/usr/bin/env python3
# @author: Markus Kösters

from .EthernetBusPlugin import Tcp_Udp_sockets, SocketConfigs
from .EthernetBusPlugin.test_UnitTests import MockSocket
from .SerialBusPlugin import SerialBus, SerialBusConfig
from .BusPluginInterface import BusPluginInterface
from .SerialBusPlugin.test_UnitTests.SerialBusMock import MockSerialBus


class BusPluginFactory:
    """
    Class for producing Bus-instances.
    """

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
        config = SerialBusConfig('/dev/ttyACM0', 115200, MockSerialBus)
        return SerialBus(config)

    @staticmethod
    def produceUdpSocketPlugin(port: int) -> Tcp_Udp_sockets.UdpSocket:
        """
        This static method initializes and produces an instance of the UdpSocket plugin
        using the provided port number and optional message size. The method acts as a
        factory for creating and returning a configured UdpSocket object.

        :param port: The port number to bind the UDP socket to.
        :type port: Int

        :return: An instance of `Tcp_Udp_sockets.UdpSocket` configured with the
            specified port and message size.
        :rtype: Tcp_Udp_sockets.UdpSocket
        """
        config: SocketConfigs = SocketConfigs.UdpSocketConfig(port=port)
        return Tcp_Udp_sockets.UdpSocket(config)

    @staticmethod
    def produceUdpStubPlugin(port: int) -> Tcp_Udp_sockets.UdpSocket:
        """
        Produces an UDP stub plugin for mock testing or emulation. This method creates a UDP
        socket configuration and initializes an UDP socket instance using a mock socket library.

        :param port: The port number to initialize the UDP socket configuration.
        :type port: Int
        :return: An instance of UdpSocket configured with the specified port and using
                 the mock socket library.
        :rtype: Tcp_Udp_sockets
        """
        config: SocketConfigs = SocketConfigs.UdpSocketConfig(port=port, busLibrary=MockSocket)
        return Tcp_Udp_sockets.UdpSocket(config)
