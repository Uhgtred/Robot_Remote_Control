from BusTransactions.Encoding.EncodingProtocol import EncodingProtocol


class PythonEncoder(EncodingProtocol):

    @staticmethod
    def decode(message: bytes) -> str:
        """
        Method for decoding a message received from a socket.
        :param message: Message from socket that needs to be decoded.
        """
        if isinstance(message, bytes):
            message = message.decode()
        return message

    @staticmethod
    def encode(message: str) -> bytes:
        """
        Method for encoding a message that will be sent to a socket.
        :param message: Message that needs to be encoded.
        """
        if not isinstance(message, bytes):
            return message.encode()
        return message