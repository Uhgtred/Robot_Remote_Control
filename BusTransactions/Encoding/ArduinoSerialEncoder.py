from BusTransactions.Encoding.EncodingProtocol import EncodingProtocol


class ArduinoSerialEncoder(EncodingProtocol):
    """
    Protocol for prescribing the structure of the encoding.
    """

    @staticmethod
    def decode(message: bytes) -> str:
        """
        Method for decoding a message received from a bus.
        :param message: Message from bus that needs to be decoded.
        """
        if isinstance(message, bytes):
            message = message.decode()
        if message.endswith('&'):
            message = message[:-1]
        return message

    @staticmethod
    def encode(message: str) -> bytes:
        """
        Method for encoding a message that will be sent to a bus.
        :param message: Message that needs to be encoded.
        """
        if not isinstance(message, bytes):
            message = f'{message}&'.encode()
        return message