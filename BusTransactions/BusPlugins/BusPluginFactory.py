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
    def produceUdpSocketPlugin(port: int, host: bool, ipAddress: str = '127.0.0.1', messageSize: int = 4096) -> Tcp_Udp_sockets.UdpSocket:
        """
        Method for creating an instance of an Udp-socket connection.
        :return: Socket-instance.
        """
        config = SocketConfigs.UdpSocketConfig(IPAddress=ipAddress, messageSize=messageSize, port=port, host=host)
        return Tcp_Udp_sockets.UdpSocket(config)

    @staticmethod
    def produceUdpStubPlugin(port: int, host: bool, ipAddress='127.0.0.1', messageSize=4096) -> Tcp_Udp_sockets:
        config = SocketConfigs.UdpSocketConfig(host=host, IPAddress=ipAddress, messageSize=messageSize, port=port, busLibrary=MockSocket)
        return Tcp_Udp_sockets.UdpSocket(config)
