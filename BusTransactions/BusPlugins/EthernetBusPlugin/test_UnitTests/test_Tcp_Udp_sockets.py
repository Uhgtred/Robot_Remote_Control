#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import BusPluginFactory


class MyTestCase(unittest.TestCase):
    # print(MockBus)
    # print(config)
    bus = BusPluginFactory.produceUdpStubPlugin(host=True, port=2101)
    testString = b'Hello World'

    def test_write(self):
        self.bus.writeBus(self.testString)
        message = self.bus.sock.buffer.pop(0)
        self.assertIn(self.testString, message)

    def test_read(self):
        self.bus.writeBus(self.testString)
        message = self.bus.readBus()
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
