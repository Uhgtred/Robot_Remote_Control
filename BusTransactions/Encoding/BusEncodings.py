#!/usr/bin/env python3
# @author Markus Kösters
import json
from typing import Protocol

import cv2
import msgpack
import numpy

import logging

class EncodingProtocol(Protocol):
    """
    Protocol for prescribing the structure of the encoding.
    """

    @staticmethod
    def decode(message: bytes) -> any:
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


class SocketEncoding(EncodingProtocol):

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


class SocketEncodingJson(EncodingProtocol):

    __logger: logging.getLogger = logging.getLogger(__name__)

    @staticmethod
    def decode(message: bytes) -> dict:
        """
        Method for decoding a message received from a socket.
        :param message: Message from socket that needs to be decoded.
        """
        SocketEncodingJson.__logger.debug(f'Message that will be decoded is of type: {type(message)}')
        if isinstance(message, bytes):
            message: json = message.decode()
        SocketEncodingJson.__logger.debug(f'Decoded message that will be unpacked from json is: {message}, of type: '
                                          f'{type(message)}')
        return json.loads(message)

    @staticmethod
    def encode(message: any) -> json:
        """
        Method for encoding a message that will be sent to a socket.
        :param message: Message that needs to be encoded.
        """
        return json.dumps(message).encode()


class ImageDataAsMsgPackEncoding(EncodingProtocol):

    __logger: logging.getLogger = logging.getLogger(__name__)

    @staticmethod
    def encode(imageData: numpy.ndarray) -> bytes:
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
        ImageDataAsMsgPackEncoding.__logger.debug(f'Serializing image data of type {type(imageData)} ...')
        encodingParameters = [int(cv2.IMWRITE_JPEG_QUALITY), 80] # 80 is the quality of the jpeg compression
        ImageDataAsMsgPackEncoding.__logger.debug(f'Encoding parameters: {encodingParameters}, imageDataType: {type(imageData)}')
        returnValue, buffer = cv2.imencode('.jpg', imageData, encodingParameters) # returnValue is type boolean.
        serializedData: bytes = msgpack.packb({'frameData': buffer.tobytes()})
        return serializedData

    @staticmethod
    def decode(data: bytes) -> any:
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
        ImageDataAsMsgPackEncoding.__logger.debug(f'Image-data that will be decoded: {data}')
        payload: any = msgpack.unpackb(data)
        frameData = payload.get('frameData')  # Access the frame
        ImageDataAsMsgPackEncoding.__logger.debug(f'Decoding image data of type {type(frameData)} ...')
        frameData: numpy.ndarray = numpy.frombuffer(frameData, dtype=numpy.uint8) # or numpy.ndarray?
        imageframe: numpy.ndarray = cv2.imdecode(frameData, cv2.IMREAD_COLOR)
        return imageframe


class NoEncoding(EncodingProtocol):
    """
    Provides a no-operation encoding and decoding protocol.

    This class implements the EncodingProtocol but does not alter the data
    during encoding or decoding. It ensures that the input and output are
    identical. Useful in scenarios where no transformation of the data
    is required.
    """

    @staticmethod
    def encode(message: any) -> any:
        """
        Encodes the provided message and returns it. This method is a placeholder,
        demonstrating a simple implementation that takes any input and directly
        returns it without any modifications.

        :param message: The message to be encoded.
        :type message: Any
        :return: The same message that was provided as input.
        :rtype: Any
        """
        return message

    @staticmethod
    def decode(message: any) -> any:
        """
        Decodes the given message and returns the same as output. This function
        can handle any type of input for the `message` parameter, and it returns
        the exact same type that was inputted. This static method does not
        modify or process the input in any substantial way, serving primarily
        as a placeholder or identity function.

        :param message: The input message of any type that will be returned
                        directly.
        :return: The input message is returned as-is without any modification.
        """
        return message