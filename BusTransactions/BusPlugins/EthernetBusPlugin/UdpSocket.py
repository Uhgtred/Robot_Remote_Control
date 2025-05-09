#!/usr/bin/env python3
# @author: Markus Kösters

import atexit
import socket

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
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('UdpSocket',
                                                                      'UdpSocket.log').getLogger

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
        data = self.__receiver()
        self.__logger.debug(f'Received data: {data}.')
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
        self.sock.sendto(message, (self.__yourIPAddress, self.__port))

    def _setupSocket(self, sock: socket, port: int) -> None:
        """
        Private Method for setting up UDP-socket.
        This method is being called on instancing this class.
        There should be no reason to call it directly.
        :param sock: Socket that will be setup and bound.
        """
        self.__logger.debug(f'Ports that are already in use: {self.__openSocketPorts}')
        if port in self.__openSocketPorts:
            # Raising exception if port is already in use, so that conflicts can be avoided.
            raise BaseException('Port already in use')
        # Creating a udp-socket object.
        self.sock: socket.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        self.__logger.debug(f'Trying to bind to Address: {self.__myIPAddress}:{port}.')
        # Binding the socket with provided address and port. It can be used for transmission and receiving now.
        self.sock.bind((self.__myIPAddress, port))
        # Adding port to the set of open sockets.
        self.__openSocketPorts.add(port)

    def __receiver(self) -> bytes | None:
        """
        Receives a message from a UDP socket and returns the message if it is received from the expected IP
        and port. Otherwise, it logs the discrepancy and returns None. This is used to ensure communication
        only with the specified network endpoint.

        :raises OSError: If there is an issue with the underlying socket operations.

        :return: The received message as a bytes object, or None if the message is not from the expected
                 network endpoint.
        :rtype: bytes | None
        """
        message, address = self.sock.recvfrom(self.__maxMessageSize)
        self.__logger.debug(f'Received message from {address}, expected {self.__yourIPAddress}:{self.__port}.')
        # Returning data only if it is received from the expected IP-Address (for safety).
        return None if address != (self.__yourIPAddress, self.__port) else message

    def close(self) -> None:
        """
        Method for closing the sockets that are still opened.
        """
        self.__logger.debug(f'Shutting down the socket with port: {self.__port}')
        self.sock.close()
        if self.__port in self.__openSocketPorts:
            self.__openSocketPorts.remove(self.__port)