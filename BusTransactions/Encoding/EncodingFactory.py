#!/usr/bin/env python3
# @author Markus Kösters

from . import BusEncodings


class EncodingFactory:
    """
    Container to make all Encodings available through one object.
    """

    @staticmethod
    def arduinoSerialEncoding():
        return BusEncodings.ArduinoSerialEncoding()

    @staticmethod
    def socketEncoding(pickle:bool):
        if pickle:
            return BusEncodings.SocketEncodingJson()
        return BusEncodings.SocketEncoding()
