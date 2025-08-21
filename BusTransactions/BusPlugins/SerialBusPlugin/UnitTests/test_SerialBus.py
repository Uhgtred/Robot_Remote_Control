#!/usr/bin/env python3
# @author Markus Kösters

import unittest

from ..SerialBusConfig import SerialBusConfig
from ..SerialBus import SerialBus
from .SerialBusMock import MockSerialBus


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # print(MockBus)
        self.config = SerialBusConfig('test', 123, MockSerialBus)
        # print(config)
        self.bus = SerialBus(self.config)
        self.testString = b'Hello World'

    def test_write(self):
        self.bus.writeBus(self.testString)
        message = self.bus.serialBus.buffer.pop(0)
        self.assertEqual(message, self.testString)

    def test_read(self):
        self.bus.writeBus(self.testString)
        message = self.bus.readBus()
        assert message == self.testString


if __name__ == '__main__':
    unittest.main()
