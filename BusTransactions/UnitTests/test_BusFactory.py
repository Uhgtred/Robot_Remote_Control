#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import BusPluginFactory, Bus
from BusTransactions import Encoding
from BusTransactions.BusFactory import BusFactory
from BusTransactions.BusPlugins.SerialBusPlugin.UnitTests.SerialBusMock import MockSerialBus


class MyTestCase(unittest.TestCase):

    busFactory = BusFactory()
    mockLibrary = MockSerialBus

    def test_produceBusTransceiver(self):
        encoding = Encoding.EncodingFactory.arduinoSerialEncoding
        bus = BusPluginFactory.produceSerialBusStubPlugin()
        transceiver = self.busFactory.produceCustomBusTransceiver(bus, encoding)
        self.assertIsInstance(transceiver, Bus)

if __name__ == '__main__':
    unittest.main()
