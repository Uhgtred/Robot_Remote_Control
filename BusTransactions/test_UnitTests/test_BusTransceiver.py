#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from BusTransactions import BusFactory, BusPluginFactory
from BusTransactions import Encoding


class helperClass:

    def __init__(self):
        self.args = None
        self.message = None
        self.testKwargs = None

    def helperMethod(self, message, *args, **kwargs):
        self.args = list(args)
        self.message = message
        self.testKwargs = kwargs

    def helperMethodNoArgs(self):
        # does not need to do anything since this is only used
        # to check wether the exception is being raised
        pass


class test_BusTransceiver(unittest.TestCase):
    bus = BusPluginFactory.produceSerialBusStubPlugin()
    serialTransceiver = BusFactory.BusFactory.produceBusTransceiver(bus, Encoding.EncodingFactory.arduinoSerialEncoding)
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
        udpBus = BusFactory.BusFactory.produceUDP_TransceiverStub(2121, True)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        udpBus.readBusUntilStopFlag(obj.helperMethod, arg, testKwarg='testKwarg')
        # letting bus init before closing. Otherwise there is an issue that the message is not correctly being received.
        time.sleep(.0001)
        udpBus.stopFlag = True
        self.assertEqual(obj.message, self.testString)
        self.assertEqual(obj.args[0], arg)
        self.assertEqual(obj.testKwargs.get('testKwarg'), 'testKwarg')

    def test_readBusUntilStopFlagFail(self):
        obj = helperClass()
        udpBus = BusFactory.BusFactory.produceUDP_TransceiverStub(2122, True)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        self.assertRaises(TypeError, udpBus.readBusUntilStopFlag, (obj.helperMethodNoArgs, arg), testKwarg='testKwarg')


if __name__ == '__main__':
    unittest.main()
