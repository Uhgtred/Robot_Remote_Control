#!/usr/bin/env python3
# @author: Markus Kösters

import atexit
import socket
import struct

from . import SocketConfigs
from ..BusPluginInterface import BusPluginInterface


class UdpSocket(BusPluginInterface):

    __openSocketPorts: set = set()

    def __init__(self, config: SocketConfigs.UdpSocketConfig):
        self.sock = None
        self.__maxMessageSize = config.messageSize
        self.__myIPAddress = config.MyIPAddress
        self.__yourIPAddress = config.YourIPAddress
        self.__port = config.port
        self._setupSocket(config.host, config.busLibrary, config.port)
        atexit.register(self.close)

    def readBus(self) -> bytes:
        """
        Method that reads the UDP socket.
        :return: Message read from the UDP socket.
        """
        headerLength = struct.calcsize('Q') # Todo: This is not a real header for udp. look at this: https://abdesol.medium.com/udp-protocol-with-a-header-implementation-in-python-b3d8dae9a74b
        header, data = self.__receiver(headerLength)
        return data

    def writeBus(self, message: bytes) -> None:
        """
        Method for writing message to UDP socket.
        :param message: Message that will be sent to UDP-socket.
        """
        __msgLength = len(message)
        __message = struct.pack('Q', __msgLength) + message
        self.sock.sendto(__message, (self.__yourIPAddress, self.__port))

    def _setupSocket(self, host: bool, sock: socket, port: int) -> None:
        """
        Private Method for setting up UDP-socket.
        This method is being called on instancing this class.
        There should be no reason to call it directly.
        :param sock: Socket that will be setup and bound.
        """
        # dynamically providing socket-ports for requested sockets.
        if port in self.__openSocketPorts:
            # check if the busLibrary-object has already been instanced
            raise BaseException('Port already in use')
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        if host:
            self.sock.bind((self.__myIPAddress, port))
            self.__openSocketPorts.add(port)

    def __receiver(self, headerLength: int | None) -> tuple[bytes, bytes]:
        """
        Method that reads from a socket either message-header or message-body.
        :param msgLength: Length of the message that will be read from the socket.
                            Length of the body is represented by the header, which has length(struct.calcsize('Q')).
        :return: Message in bytes format.
        """
        message, address = self.sock.recvfrom(self.__maxMessageSize)
        header, data = message[:headerLength], message[headerLength:]
        return header, data

    def close(self) -> None:
        """
        Method for closing the socket.
        """
        self.sock.close()
        self.__openSocketPorts.remove(self.__port)