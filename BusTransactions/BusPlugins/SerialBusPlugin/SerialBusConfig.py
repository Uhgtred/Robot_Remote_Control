#!/usr/bin/env python3
# @author: Markus Kösters
from dataclasses import dataclass

import serial


@dataclass
class SerialBusConfig:
    """
    Represents the configuration for a serial bus communication.

    This class encapsulates the configuration necessary for setting up
    serial communication. It specifies the port, baud rate, and the library
    used for handling serial communication.

    :ivar port: The port identifier for the serial communication.
    :type port: str
    :ivar baudRate: The communication speed in bits per second.
    :type baudRate: int
    :ivar busLibrary: The serial library used for communication. Defaults
        to `serial.Serial`.
    :type busLibrary: serial.Serial
    """
    port: str
    baudRate: int
    busLibrary: serial.Serial = serial.Serial
