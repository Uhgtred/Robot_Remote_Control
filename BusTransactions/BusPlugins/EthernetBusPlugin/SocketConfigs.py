#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Config-dataclass for Serial-busses.
    """
    IPAddress: str
    messageSize: int
    port: int
    host: bool
    busLibrary: socket = socket
