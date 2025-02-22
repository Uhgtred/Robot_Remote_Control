#!/usr/bin/env python3
# @author Markus Kösters
import json
from typing import Protocol

import cv2
import msgpack
import numpy

from ProjectLogging import Logger


class EncodingProtocol(Protocol):
    """
    Protocol for prescribing the structure of the encoding.
    """

    @staticmethod
    def decode(message: any) -> any:
        """
        Method for decoding a message received from a bus.
        :param message: Message from bus that needs to be decoded.
        """
        pass

    @staticmethod
    def encode(message: any) -> any:
        """
        Method for encoding a message that will be sent to a bus.
        :param message: Message that needs to be encoded.
        """
        pass


class ArduinoSerialEncoding(EncodingProtocol):
    """
    Protocol for prescribing the structure of the encoding.
    """

    @staticmethod
    def decode(message: any) -> str:
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


class SocketEncoding(EncodingProtocol):

    @staticmethod
    def decode(message: any) -> str:
        """
        Method for decoding a message received from a socket.
        :param message: Message from socket that needs to be decoded.
        """
        if isinstance(message, bytes):
            message = message.decode()
        return message

    def encode(self, message: str) -> bytes:
        """
        Method for encoding a message that will be sent to a socket.
        :param message: Message that needs to be encoded.
        """
        if not isinstance(message, bytes):
            return message.encode()
        return message


class SocketEncodingJson(EncodingProtocol):

    @staticmethod
    def decode(message: json) -> dict:
        """
        Method for decoding a message received from a socket.
        :param message: Message from socket that needs to be decoded.
        """
        return json.loads(message.decode())

    def encode(self, message: any) -> json:
        """
        Method for encoding a message that will be sent to a socket.
        :param message: Message that needs to be encoded.
        """
        return json.dumps(message.getButtonDict).encode()


class ImageDataAsMsgPackEncoding(EncodingProtocol):

    def __init__(self):
        self.__logger: Logger.getLogger = Logger('SerializerMsgPack','SerializerLog.log').getLogger

    def encode(self, imageData: numpy.ndarray) -> bytes:
        """
        Serialize raw image data into a compressed byte format.

        This function takes a NumPy ndarray representing image data, compresses it
        using JPEG encoding, and serializes it into a compact byte format using msgpack.
        The result includes the compressed image data in encoded byte array format,
        suitable for network transmission or storage.

        :param imageData: A NumPy ndarray containing raw image data to be serialized.
        :type imageData: numpy.ndarray
        :return: A serialized byte object containing the compressed image data in
            msgpack format.
        :rtype: bytes
        """
        # This makes the code use the abstract method at the beginning, which includes a little bit of error-handling.
        self.__logger.debug(f'Serializing image data of type {type(imageData)} ...')
        encodingParameters = [int(cv2.IMWRITE_JPEG_QUALITY), 80] # 80 is the quality of the jpeg compression
        returnValue, buffer = cv2.imencode('.jpg', imageData, encodingParameters) # returnValue is type boolean.
        serializedData: bytes = msgpack.packb({'frameData': buffer.tobytes()})
        return serializedData

    def decode(self, data: bytes) -> any:
        """
        Decodes a given byte data utilizing msgpack unpacking and OpenCV decoding to
        obtain an image frame.

        This function processes serialized byte data (in msgpack format), unpacks it,
        extracts frame data, converts it into an array, and finally decodes the image
        data with OpenCV's imdecode function. The returned result is the image frame.

        :param data: Encoded byte data that contains serialized image frame information.
        :type data: bytes
        :return: Decoded image frame extracted from the provided byte data.
        :rtype: any
        """
        payload = msgpack.unpackb(data)
        frameData = payload.get(b'frameData')  # Access the frame
        frameData = numpy.frombuffer(frameData, dtype=numpy.uint8) # or numpy.ndarray?
        imageframe = cv2.imdecode(frameData, cv2.IMREAD_COLOR)
        return imageframe

