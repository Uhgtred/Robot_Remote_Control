#!/usr/bin/env python3
# @author: Markus Kösters

import socket
import struct

from . import SocketConfigs
from ..BusPluginInterface import BusPluginInterface


class UdpSocket(BusPluginInterface):

    # Todo: Implement possibility to close Socket. It will be necessary to remove it from the openPorts list as well.
    #       Also there needs to be a limit on how many sockets can be opened simultaneously!
    __openSocketPorts: list = []

    def __init__(self, config: SocketConfigs.UdpSocketConfig):
        sockLibrary = config.busLibrary
        self.sock = None
        self.__messageSize = config.messageSize
        self.__address = config.IPAddress
        self._setupSocket(sockLibrary)

    def readBus(self) -> bytes:
        """
        Method that reads the UDP socket.
        :return: Message read from the UDP socket.
        """
        # --- Receiving header containing message-length --- #
        headerLength = struct.calcsize('Q')
        # running loop until size of message-length (headerLength (8byte)) has been reached
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
        self.sock.sendto(__message, self.__address)

    def _setupSocket(self, sock: socket) -> None:
        """
        Private Method for setting up UDP-socket.
        :param sock: socket that will be setup and bound.
        """
        # dynamically providing socket-ports for requested sockets.
        sockPort = 2001
        while sockPort in self.__openSocketPorts:
            sockPort += 1
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        self.sock.bind((self.__address, sockPort))
        self.__openSocketPorts.append(sockPort)

    def __receiver(self, msgLength: int) -> bytes:
        """
        Method that reads from a socket either message-header or message-body.
        :param msgLength: Length of the message that will be read from the socket.
                            Length for the body is represented by the header, which has length(struct.calcsize('Q')).
        :return: Message in bytes format.
        """
        data = b''
        while len(data) < msgLength:
            # varying receive-length to only receive the bytes of this specific message
            rcvSize = msgLength - len(data)
            # receiving dynamic size of packets until every byte has been received
            packet = self.sock.recvfrom(rcvSize if rcvSize <= msgLength else msgLength)
            if not packet:
                break
            data += packet
        return data
