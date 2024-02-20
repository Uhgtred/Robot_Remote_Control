#!/usr/bin/env python3
# @author: Markus Kösters

from .EthernetBusPlugin import Tcp_Udp_sockets, SocketConfigs
from .SerialBusPlugin import SerialBus, SerialBusConfig
from .BusPluginInterface import BusPluginInterface
from .SerialBusPlugin.test_UnitTests.SerialBusMock import MockSerialBus


class BusPluginFactory:
    """
    Class for producing Bus-instances.
    """

    @staticmethod
    def produceSerialBusArduinoPlugin() -> BusPluginInterface:
        """
        Method for creating an instance of a SerialBus.
        :return: SerialBus-instance.
        """
        config = SerialBusConfig('/dev/ttyACM0', 115200)
        return SerialBus(config)

    @staticmethod
    def produceSerialBusStubPlugin() -> BusPluginInterface:
        config = SerialBusConfig('/dev/ttyACM0', 115200, MockSerialBus)
        return SerialBus(config)

    @staticmethod
    def produceUdpSocketPlugin(ipAddress='127.0.0.1', messageSize=4096) -> BusPluginInterface:
        """
        Method for creating an instance of a Udp-socket connection.
        :return: Socket-instance.
        """
        config = SocketConfigs.UdpSocketConfig(IPAddress=ipAddress, messageSize=messageSize)
        return Tcp_Udp_sockets.UdpSocket(config)

    @staticmethod
    def produceUdpStubPlugin(ipAddress='127.0.0.1', messageSize=4096) -> BusPluginInterface:
        config = SocketConfigs.UdpSocketConfig(IPAddress=ipAddress, messageSize=messageSize, socketClass=MockUdpSocket)
        return Tcp_Udp_sockets.UdpSocket(config)
