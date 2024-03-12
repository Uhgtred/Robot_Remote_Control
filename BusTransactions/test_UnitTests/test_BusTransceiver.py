#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from BusTransactions import BusFactory, BusPluginFactory
from BusTransactions import Encoding

class helperClass:

    args = None
    message = None
    testKwargs = None

    def helperMethod(self, message, *args, **kwargs):
        self.args = list(args)
        self.message = message
        self.testKwargs = kwargs

    def helperMethodNoArgs(self):
        pass


class MyTestCase(unittest.TestCase):
    busFactory = BusFactory.BusFactory()
    bus = BusPluginFactory.produceSerialBusStubPlugin()
    serialTransceiver = busFactory.produceBusTransceiver(bus, Encoding.EncodingFactory.arduinoSerialEncoding)
    testString = 'Test from BusTransceiver'
    messages = []

    def test_BusTransceiver_writeSingleMessage(self):
        self.serialTransceiver.writeSingleMessage(self.testString)
        message = self.serialTransceiver.bus.bus.buffer.pop(0)
        self.assertEqual(message[:-1], self.testString.encode())

    def test_BusTransceiver_readSingleMessage(self):
        self.serialTransceiver.writeSingleMessage(self.testString)
        message = self.serialTransceiver.readSingleMessage()
        self.assertEqual(message, self.testString)

    def test_readBusUntilStopFlag(self):
        obj = helperClass()
        udpBus = self.busFactory.produceUDP_TransceiverStub(2007, True)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        udpBus.readBusUntilStopFlag(obj.helperMethod, arg, testKwarg='testKwarg')
        udpBus.stopFlag = True
        self.assertEqual(obj.message, self.testString)
        self.assertEqual(obj.args[0], arg)
        self.assertEqual(obj.testKwargs.get('testKwarg'), 'testKwarg')

    def test_readBusUntilStopFlagFail(self):
        obj = helperClass()
        udpBus = self.busFactory.produceUDP_TransceiverStub(2007, True)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        self.assertRaises(TypeError, udpBus.readBusUntilStopFlag, (obj.helperMethodNoArgs, arg), testKwarg='testKwarg')


if __name__ == '__main__':
    unittest.main()
