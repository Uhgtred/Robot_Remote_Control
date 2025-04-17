#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import BusPluginFactory, Bus
from BusTransactions import Encoding
from BusTransactions.DefaultBusFactory import DefaultBusFactory
from BusTransactions.BusPlugins.SerialBusPlugin.UnitTests.SerialBusMock import MockSerialBus


class MyTestCase(unittest.TestCase):

    busFactory = DefaultBusFactory()
    mockLibrary = MockSerialBus

    def test_produceBusTransceiver(self):
        encoding = Encoding.EncodingFactory.arduinoSerialEncoding
        bus = BusPluginFactory.produceSerialBusStubPlugin()
        transceiver = self.busFactory.produceCustomBusTransceiver(bus, encoding)
        self.assertIsInstance(transceiver, Bus)

if __name__ == '__main__':
    unittest.main()
