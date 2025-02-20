#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Config-dataclass for Serial-busses.
    """
    port: int
    messageSize: int = 4096
    MyIPAddress: str = '192.168.178.32'
    YourIPAddress: str = '192.168.178.36'
    busLibrary: socket = socket
