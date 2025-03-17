#!/usr/bin/env python3
# @author: Markus Kösters

import json
import unittest

import cv2
import msgpack
import numpy

import ProjectLogging
from BusTransactions import EncodingFactory
from BusTransactions.Encoding import EncodingProtocol


class TestBusEncodings(unittest.TestCase):

    def setUp(self):
        self.encoding = EncodingFactory
        self.__logger: ProjectLogging = ProjectLogging.Logger('TestBusEncodings',
                                                              'TestBusEncodings.log').getLogger

    def test_jsonDecoding(self):
        message: bytes = json.dumps({'testKey': 'testValue'}).encode()
        encoder:  EncodingProtocol = self.encoding.socketEncoding('json')
        decodedJsonData = encoder.decode(message)
        self.assertIsInstance(decodedJsonData, dict)

    def test_jsonEncoding(self):
        message: dict = {'testKey': 'testValue'}
        self.__logger.debug(f'Raw data before encoding is of type: {type(message)}.')
        encoder: EncodingProtocol = self.encoding.socketEncoding('json')
        encodedJsonData = encoder.encode(message)
        self.__logger.debug(f'Encoded message is of type: {type(encodedJsonData)}')
        self.assertIsInstance(encodedJsonData, bytes)

    def test_pythonInternalEncoding(self):
        message: str = 'Hello World'
        self.__logger.debug(f'Raw data before encoding is of type: {type(message)}.')
        encoder: EncodingProtocol = self.encoding.socketEncoding('pythonDefault')
        encodedStringData = encoder.encode(message)
        self.__logger.debug(f'Encoded message is of type: {type(encodedStringData)}')
        self.assertIsInstance(encodedStringData, bytes)

    def test_pythonInternalDecoding(self):
        message: bytes = 'Hello World'.encode()
        encoder: EncodingProtocol = self.encoding.socketEncoding('pythonDefault')
        decodedStringData = encoder.decode(message)
        self.assertIsInstance(decodedStringData, str)

    def test_arduinoSerialEncoding(self):
        message: str = 'Hello World'
        self.__logger.debug(f'Raw data before encoding is of type: {type(message)}.')
        encoder: EncodingProtocol = self.encoding.arduinoSerialEncoding()
        encodedStringData = encoder.encode(message)
        self.__logger.debug(f'Encoded message is of type: {type(encodedStringData)}')
        self.assertIsInstance(encodedStringData, bytes)

    def test_arduinoSerialDecoding(self):
        message: bytes = 'Hello World'.encode()
        encoder: EncodingProtocol = self.encoding.arduinoSerialEncoding()
        decodedStringData = encoder.decode(message)
        self.assertIsInstance(decodedStringData, str)

    def test_VideoDataDecoding(self):
        # Create a valid image with shape (10, 10, 3) for RGB
        imageData: numpy.ndarray = numpy.ones((10, 10, 3), dtype=numpy.uint8) * 255  # White image
        encodingParameters: list[int] = [int(cv2.IMWRITE_JPEG_QUALITY), 80]  # 80 is the quality of the jpeg compression
        returnValue, buffer = cv2.imencode('.jpg', imageData, encodingParameters)  # returnValue is type boolean.
        serializedData: bytes = msgpack.packb({'frameData': buffer.tobytes()})
        self.__logger.debug(f'Image-Data that is going to be decoded: {type(serializedData)}.')
        imageEncoder: EncodingProtocol = self.encoding.produceImageReceiverEncoding()
        decodedImageData = imageEncoder.decode(serializedData)
        self.__logger.debug(f'Type of the decoded image-data is: {type(decodedImageData)}.')

    def test_VideoEncoding(self):
        imageData: numpy.ndarray = numpy.ones((10, 10, 3), dtype=numpy.uint8) * 255  # White image
        self.__logger.debug(f'Raw image-data before encoding is of type: {type(imageData)}.')
        imageEncoder: EncodingProtocol = self.encoding.produceImageReceiverEncoding()
        encodedImageData = imageEncoder.encode(imageData)
        self.__logger.debug(f'Encoded image-data is of type: {type(encodedImageData)}.')
        self.assertIsInstance(encodedImageData, bytes)


if __name__ == '__main__':
    unittest.main()
