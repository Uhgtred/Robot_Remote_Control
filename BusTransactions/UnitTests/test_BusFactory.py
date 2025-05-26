#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.BusPlugins.SerialBusPlugin.UnitTests.SerialBusMock import MockSerialBus
from BusTransactions.DefaultBusFactory import DefaultBusFactory


class MyTestCase(unittest.TestCase):

    busFactory = DefaultBusFactory()
    mockLibrary = MockSerialBus

    def test_produceBusTransceiver(self):
        transceiver: AbstractBus = self.busFactory.produceUDP_Transceiver(1234)
        self.assertIsInstance(transceiver, AbstractBus)


if __name__ == '__main__':
    unittest.main()
