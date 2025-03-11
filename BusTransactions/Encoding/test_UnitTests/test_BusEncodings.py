#!/usr/bin/env python3
# @author: Markus Kösters
import inspect
import unittest

import ProjectLogging
from BusTransactions import EncodingFactory


class test_BusEncodings(unittest.TestCase):

    def setUp(self):
        self.encoding = EncodingFactory
        self.__logger: ProjectLogging = ProjectLogging.Logger('TestBusEncodings', 'TestBusEncodings.log').getLogger

    def test_decode(self):
        """
        Testing any decodings in Encodinginterface, that follow the protocol:
        EncodingProtocol
        """
        tests = []
        for method in dir(self.encoding):
            self.__logger.debug(f'The encoding that is going to be tested is: {method}')
            if not method.startswith('__'):
                method = getattr(self.encoding, method)()
                message = b'Hello World'
                self.__logger.debug(f'The message that is going to be decoded is: {message}')
                message = method.decode(message)
                tests.append(type(message))
        assert bytes not in tests

    def test_encode(self):
        """
        Testing any encodings in Encodinginterface, that follow the protocol:
        EncodingProtocol
        """
        tests = []
        for method in dir(self.encoding):
            if not method.startswith('__'):
                method = getattr(self.encoding, method)()
                message = 'Hello World'
                message = method.encode(message)
                tests.append(type(message))
        assert str not in tests and bytes in tests


if __name__ == '__main__':
    unittest.main()
