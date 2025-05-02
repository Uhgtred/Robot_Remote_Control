import json

import ProjectLogging
from BusTransactions.Encoding.EncodingProtocol import EncodingProtocol


class SocketEncoderJson(EncodingProtocol):

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('SocketEncoderJson',
                                                                      'SocketEncoderJson.log').getLogger

    @staticmethod
    def decode(message: bytes) -> dict:
        """
        Method for decoding a message received from a socket.
        :param message: Message from socket that needs to be decoded.
        """
        SocketEncoderJson.__logger.debug(f'Message that will be decoded is of type: {type(message)}')
        if isinstance(message, bytes):
            message: json = message.decode()
        SocketEncoderJson.__logger.debug(f'Decoded message that will be unpacked from json is: {message}, of type: '
                                          f'{type(message)}')
        return json.loads(message)

    @staticmethod
    def encode(message: any) -> json:
        """
        Method for encoding a message that will be sent to a socket.
        :param message: Message that needs to be encoded.
        """
        return json.dumps(message).encode()