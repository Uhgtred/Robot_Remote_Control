#!/usr/bin/env python3
# @author Markus Kösters

from . import BusEncodings


class EncodingFactory:
    """
    Factory class to provide encoding strategies for Arduino Serial communication
    and socket-based communication.

    This class serves as a centralized factory for creating instances of encoding
    mechanisms used in different communication scenarios. It offers utility methods
    to return the specific encoding strategy based on the given requirements.

    """

    @staticmethod
    def arduinoSerialEncoding() -> BusEncodings:
        """
        Static method that provides the BusEncoding implementation specific to
        Arduino Serial communication. This encoding is suitable for scenarios
        where Arduino devices interact with other components using serial
        protocols. It ensures the format aligns with the needs of such low-level
        communication.

        :rtype: BusEncodings
        :return: The encoding implementation tailored for Arduino Serial
                 communication.
        """
        return BusEncodings.ArduinoSerialEncoding()

    @staticmethod
    def socketEncoding(encodingType: str = "json") -> BusEncodings:
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
            case "json": return BusEncodings.SocketEncodingJson()
            case "pythonDefault": return BusEncodings.SocketEncoding()
            case default: return BusEncodings.SocketEncodingJson()

    @staticmethod
    def produceImageReceiverEncoding() -> BusEncodings:
        """
        Statically produces an instance of `BusEncodings` that represents the encoding
        for image data as MessagePack encoding. The method constructs and returns a suitable
        encoding for image data to be utilized in message bus communication.

        :return: An instance of `BusEncodings` configured for image data with MessagePack encoding.
        """
        return BusEncodings.ImageDataAsMsgPackEncoding()
