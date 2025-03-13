#!/usr/bin/env python3
# @author: Markus Kösters

import ProjectLogging
from BusTransactions.BusPlugins.EthernetBusPlugin import UdpSocketConfig


class MockSocket:
    """
    Simulates the behavior of a network socket for testing purposes.

    The MockSocket class is designed to replicate the typical functionality of a network
    socket, enabling developers to simulate and test scenarios involving socket communication
    without using actual network resources. It includes methods for sending and receiving
    data, binding to addresses, and managing socket states. Additionally, it logs operations
    for debugging purposes.

    :ivar buffer: A class-level list simulating the internal message buffer for the socket.
    :type buffer: list
    :ivar state: A class-level boolean indicating the current state of the socket.
    :type state: bool
    :ivar AF_INET: A class-level placeholder for the Internet address family.
    :type AF_INET: NoneType
    :ivar SOCK_STREAM: A class-level placeholder for the stream socket type.
    :type SOCK_STREAM: NoneType
    :ivar SOCK_DGRAM: A class-level placeholder for the datagram socket type.
    :type SOCK_DGRAM: NoneType
    :ivar passedArgs: A list to hold additional arguments passed to the socket.
    :type passedArgs: list
    :ivar port: The port number associated with the socket.
    :type port: int
    :ivar address: The IP address associated with the socket.
    :type address: str
    :ivar __logger: An internal logger instance for recording debug messages.
    :type __logger: ProjectLogging.Logger.getLogger
    """

    buffer = []
    state = False
    AF_INET = None
    SOCK_STREAM = None
    SOCK_DGRAM = None
    passedArgs = []
    address: tuple[str, int] = None
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('MockSocket', 'MockSocket.log').getLogger

    def __init__(self, *args, **kwargs):
        self.passedArgs.extend(args)
        self.passedArgs.extend(kwargs)

    @classmethod
    def recvfrom(cls, messageSize):
        """
        Receives a specific number of bytes as defined by messageSize. Retrieves data from a
        buffer if it exists, and ensures proper handling of the buffer by managing message
        overflow. If the buffer is empty, a predefined message is returned instead.

        :param messageSize: The number of bytes to be received from the message buffer.
        :type messageSize: int
        :return: A tuple consisting of the received message of the specified size and the
            associated address.
        :rtype: tuple
        """
        cls.__logger.debug(f'Receiving {messageSize} bytes.')
        if cls.buffer:
            message = cls.buffer.pop(0)
            if len(message[messageSize:]) > 0:
                cls.buffer.append(message[messageSize:])
            cls.__logger.debug(f'Received message: {message}')
            return message[:messageSize], cls.address
        else:
            cls.__logger.debug('No messages in buffer. Returning some predefined message.')
            return 'Some predefined message.', cls.address

    @staticmethod
    def bind(address):
        """
        Binds the mock socket to a specified address. This method emulates the behavior of a
        real socket's `bind` method, logging the provided address for debugging purposes.

        :param address: The address to which the mock socket will be bound.
        :type address: Any
        :return: None
        """
        MockSocket.__logger.debug(f'Address of socket: {address}')

    @classmethod
    def socket(cls, *args):
        """
        Changes the state of the class and returns the class itself.

        This method toggles the state of the class. If the current state is
        set to True, it switches the state to False. If the current state
        is set to False, it switches the state to True. This method
        returns the class after changing its state.

        :param args: Additional arguments passed to the method.
        :return: The class itself after toggling the state.
        :rtype: type
        """
        if cls.state:
            cls.state = True
        else:
            cls.state = False
        return cls

    @classmethod
    def close(cls):
        """
        Represents a mechanism to modify and manage the state related to a specific class.
        This method is used to set the state of the class to `False`.

        :return: None
        """
        cls.state = False

    @classmethod
    def sendto(cls, message, address):
        """
        Sends a given message to the specified address and logs the action.

        This method logs the action of sending a message to a specific socket address
        at the debug level, adds the message to an internal buffer, and
        manages the process through a class-level logger and buffer.

        :param message: The message to be sent.
        :param address: The address of the socket to which the message will be sent.
        :return: None
        """
        cls.__logger.debug(f'Sending message: {message} to socket: {address}')
        cls.address: tuple[str, int] = address
        cls.buffer.append(message)

    @property
    def getBuffer(self):
        """
        Retrieves the value of the `buffer` attribute.

        This property method provides access to the internal buffer attribute of the
        instance. The method allows for encapsulation while exposing the required
        attribute to be retrieved when needed.

        :return: The current value stored in the `buffer` attribute.
        :rtype: Any
        """
        return self.buffer
