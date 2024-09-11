#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Config-dataclass for Serial-busses.
    """
    messageSize: int
    port: int
    host: bool
    IPAddress: str = 'localhost'
    busLibrary: socket = socket
