#!/usr/bin/env python3
# @author: Markus Kösters
from dataclasses import dataclass

import serial


@dataclass
class SerialBusConfig:
    """
    Config-dataclass for Serial-busses.
    """
    port: str
    baudRate: int
    busLibrary: serial.Serial = serial.Serial
