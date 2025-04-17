#!/usr/bin/env python3
# @author Markus Kösters

from . import EncodingProtocol
from .ArduinoSerialEncoder import ArduinoSerialEncoder
from .ImageDataEncoder import ImageDataEncoder
from .PythonEncoder import PythonEncoder
from .SocketEncoderJson import SocketEncoderJson


class EncodingFactory:
    """
    Factory class to provide encoding strategies for Arduino Serial communication
    and socket-based communication.

    This class serves as a centralized factory for creating instances of encoding
    mechanisms used in different communication scenarios. It offers utility methods
    to return the specific encoding strategy based on the given requirements.

    """

    @staticmethod
    def arduinoSerialEncoding() -> EncodingProtocol:
        """
        Static method that provides the BusEncoding implementation specific to
        Arduino Serial communication. This encoding is suitable for scenarios
        where Arduino devices interact with other components using serial
        protocols. It ensures the format aligns with the needs of such low-level
        communication.

        :rtype: EncodingProtocol
        :return: The encoding implementation tailored for Arduino Serial
                 communication.
        """
        return ArduinoSerialEncoder()

    @staticmethod
    def socketEncoding(encodingType: str = "json") -> EncodingProtocol:
        """
        Determine the socket encoding strategy based on the specified encoding type.

        This static method selects the appropriate encoding mechanism for socket
        communication, depending on the input provided. If no valid encoding type
        is specified, it defaults to using JSON encoding.

        :param encodingType: The desired socket encoding type. Possible values
            include "json" and "python".
        :type encodingType: Str, optional
        :return: An object representing the encoding strategy for communication. The
            returned object corresponds to the specified encoding type, and if no
            valid type is provided, defaults to a JSON encoding strategy.
        :rtype: BusEncodings.SocketEncodingJson or BusEncodings.SocketEncoding
        """
        match encodingType:
            case "json": return SocketEncoderJson()
            case "pythonDefault": return PythonEncoder()
            case default: return SocketEncoderJson()

    @staticmethod
    def produceImageReceiverEncoding() -> EncodingProtocol:
        """
        Statically produces an instance of `BusEncodings` that represents the encoding
        for image data as MessagePack encoding. The method constructs and returns a suitable
        encoding for image data to be utilized in message bus communication.

        :return: An instance of `BusEncodings` configured for image data with MessagePack encoding.
        """
        return ImageDataEncoder()
