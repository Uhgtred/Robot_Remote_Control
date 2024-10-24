#!/usr/bin/env python3
# @author: Markus Kösters
import atexit
import json
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
        # --- Receiving header containing message-length --- #
        headerLength = struct.calcsize('Q')
        # running loop until the size of message-length (headerLength (8byte)) has been reached
        msgLength = self.__receiver(headerLength)
        # unpacking the message-length
        msgLength = int(struct.unpack('Q', msgLength)[0])
        # --- Receiving header containing message-data --- #
        msgData = self.__receiver(msgLength)
        return msgData

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
        :param sock: socket that will be setup and bound.
        """
        # dynamically providing socket-ports for requested sockets.
        if port in self.__openSocketPorts:
            raise BaseException('Port already in use')
            # check if the busLibrary-object has already been instanced
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        # self.sock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        if host:
            self.sock.bind((self.__myIPAddress, port))
            self.__openSocketPorts.add(port)

    def __receiver(self, msgLength: int) -> bytes:
        """
        Method that reads from a socket either message-header or message-body.
        :param msgLength: Length of the message that will be read from the socket.
                            Length of the body is represented by the header, which has length(struct.calcsize('Q')).
        :return: Message in bytes format.
        """
        data = b''
        while len(data) < msgLength:
            # Varying receive-length to only receive the bytes of this specific message but max. self.__maxMessageSize!
            rcvSize = self.__maxMessageSize if (msgLength - len(data)) > self.__maxMessageSize else (msgLength - len(data))
            # receiving dynamic size of packets until every byte has been received
            packet = self.sock.recvfrom(rcvSize)
            if not packet[0]:
                break
            data += packet[0]
        return data

    def close(self) -> None:
        """
        Method for closing the socket.
        """
        self.sock.close()
        self.__openSocketPorts.remove(self.__port)