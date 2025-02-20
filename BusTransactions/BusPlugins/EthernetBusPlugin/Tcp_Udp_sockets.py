#!/usr/bin/env python3
# @author: Markus Kösters

import atexit
import socket
import struct

import ProjectLogging
from . import SocketConfigs
from ..BusPluginInterface import BusPluginInterface


class UdpSocket(BusPluginInterface):
    """
    Class providing functionality for communication over a UDP socket.

    This class serves as an interface for reading from and writing to a UDP socket.
    It is initialized with configuration parameters providing details about the UDP
    connection, such as IP addresses, port number, and message size. The class abstracts
    out tasks like setting up the socket, sending messages, and receiving messages. It
    also manages socket resource cleanup upon instance termination.

    :ivar sock: The UDP socket instance used for communication.
    :type sock: socket
    :ivar __maxMessageSize: Maximum allowable size for messages transmitted or received.
    :type __maxMessageSize: int
    :ivar __myIPAddress: IP address of the local machine for binding the UDP socket.
    :type __myIPAddress: str
    :ivar __yourIPAddress: IP address of the remote machine for sending data.
    :type __yourIPAddress: str
    :ivar __port: The port number used for binding or sending data on the UDP socket.
    :type __port: int
    """

    __openSocketPorts: set = set()
    # Initializing a Logger. The loglevel can globally be set in ProjectLogging.Logger.
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('TCP_UDP_Sockets',
                                                                           'TCP_UDP_Sockets.log').getLogger

    def __init__(self, config: SocketConfigs.UdpSocketConfig):
        self.sock: socket.socket | None = None
        self.__maxMessageSize = config.messageSize
        self.__myIPAddress = config.MyIPAddress
        self.__yourIPAddress = config.YourIPAddress
        self.__port = config.port
        self._setupSocket(config.busLibrary, config.port)
        atexit.register(self.close)

    def readBus(self) -> bytes:
        """
        Reads data from a bus using a custom UDP protocol implementation. This method
        handles the extraction of a header and associated data, relying on the
        `__receiver` method to retrieve raw data.

        The header length is determined based on the size of an unsigned long long
        integer (type 'Q'), as per Python's `struct` module. After extracting the
        header portion, the method returns the remaining data payload.

        :return: The data payload received from the bus, as a sequence of bytes.
        :rtype: Bytes
        """
        self.__logger.debug(f'Reading from bus: {self.__yourIPAddress}:{self.__port}.')
        headerLength = struct.calcsize('Q')
        self.__logger.debug(f'Reading from bus with header length: {headerLength}.')
        header, data = self.__receiver(headerLength)
        self.__logger.debug(f'Received header: {header}, data: {data}.')
        return data

    def writeBus(self, message: bytes) -> None:
        """
        Sends a message through a socket connection to a specified IP address and port.

        The message is prefixed with its length represented as an 8-byte unsigned integer
        (packaged using the struct module). The full message (length + message content)
        is then sent to the assigned IP address and port.

        :param message: The data to be sent, represented as a series of bytes.
        :type message: Bytes

        :return: None
        """
        __msgLength = len(message)
        __message = struct.pack('Q', __msgLength) + message
        self.sock.sendto(__message, (self.__yourIPAddress, self.__port))

    def _setupSocket(self, sock: socket, port: int) -> None:
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
        self.sock: socket.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        self.__logger.debug(f'Trying to bind to Address: {self.__myIPAddress}:{port}.')
        self.sock.bind((self.__myIPAddress, port))
        self.__openSocketPorts.add(port)

    def __receiver(self, headerLength: int | None) -> tuple[bytes, bytes] | tuple[None, None]:
        """
        Receives a message from a socket and processes it based on the specified header length.
        Checks if the message is received from the expected IP address and port. Returns the
        header and data as separate components, or None if the address is not the expected one.

        :param headerLength: Length of the header in the received message. Determines the
            position at which the message is split into header and data. If None, no header
            processing is performed. Must be an integer or None.
        :return: A tuple containing the header and data if the message is received from the
            expected source, otherwise a tuple of None values. The header and data are bytes
            objects.
        """
        message, address = self.sock.recvfrom(self.__maxMessageSize)
        # Returning data only if it is received from the expected IP-Address.
        if address != (self.__yourIPAddress, self.__port):
            return None, None
        header, data = message[:headerLength], message[headerLength:]
        return header, data

    def close(self) -> None:
        """
        Method for closing the socket.
        """
        self.sock.close()
        self.__openSocketPorts.remove(self.__port)