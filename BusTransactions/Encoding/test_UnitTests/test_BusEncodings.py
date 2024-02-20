#!/usr/bin/env python3
# @author: Markus Kösters
import inspect
import unittest

from BusTransactions import EncodingFactory


class MyTestCase(unittest.TestCase):

    encoding = EncodingFactory

    def test_decode(self):
        """
        Testing any decodings in Encodinginterface, that follow the protocol:
        EncodingProtocol
        """
        tests = []
        for method in dir(self.encoding):
            if not method.startswith('__'):
                method = getattr(self.encoding, method)()
                message = b'Hello World'
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
