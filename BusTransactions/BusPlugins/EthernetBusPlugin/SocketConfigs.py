#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Represents the configuration of a UDP socket.

    This class encapsulates the configuration parameters required for setting up
    a UDP socket connection. It includes attributes for specifying the port,
    message size, IP addresses for both ends of the socket communication, and the
    socket library to be used.

    :ivar port: The port number used for the UDP socket.
    :type port: int
    :ivar messageSize: The maximum size of the message to be sent or received.
    :type messageSize: int
    :ivar MyIPAddress: The IP address of the local device running the script.
    :type MyIPAddress: str
    :ivar YourIPAddress: The IP address of the remote device to be connected.
    :type YourIPAddress: str
    :ivar busLibrary: The library used for socket communication.
    :type busLibrary: socket
    """
    port: int
    messageSize: int = 4096
    # IP-Address of the device that this script is running on
    MyIPAddress: str = '192.168.178.36'
    # IP-Address of the device that will be connected to the socket from the other side.
    YourIPAddress: str = '192.168.178.32'
    busLibrary: socket = socket
