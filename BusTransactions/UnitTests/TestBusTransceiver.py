#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from BusTransactions import BusFactory, BusPluginFactory
from BusTransactions import Encoding


class helperClass:
    """
    Represents a helper class for managing messages, arguments, and keyword arguments.

    Provides methods to process and store input messages, arguments, and keywords,
    and supports additional functionality for specific use cases.

    :ivar args: Stores the list of arguments passed to `helperMethod`.
    :type args: list
    :ivar message: Contains the message passed to `helperMethod`.
    :type message: str
    :ivar testKwargs: Holds the keyword arguments passed to `helperMethod`.
    :type testKwargs: dict
    """
    def __init__(self):
        self.args = None
        self.message = None
        self.testKwargs = None

    def helperMethod(self, message, *args, **kwargs):
        """
        Helper method for processing a message, positional arguments, and keyword
        arguments. This method initializes internal attributes with the provided
        data for further use.

        :param message: The main message to be processed.
        :type message: str
        :param args: Additional positional arguments passed to the method.
        :type args: tuple
        :param kwargs: Additional keyword arguments passed to the method.
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.args = list(args)
        self.message = message
        self.testKwargs = kwargs

    def helperMethodNoArgs(self):
        """
        This method is a placeholder that performs no operation. It is intended to
        test whether an exception is raised during unit testing, due to a missing argument of this method
        or other validation processes.

        :return: None
        """
        # does not need to do anything since this is only used
        # to check wether the exception is being raised
        pass


class TestBusTransceiver(unittest.TestCase):
    bus = BusPluginFactory.produceSerialBusStubPlugin()
    serialTransceiver = BusFactory.BusFactory.produceBusTransceiver(bus, Encoding.EncodingFactory.arduinoSerialEncoding)
    testString = 'Hello World'
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
        udpBus = BusFactory.BusFactory.produceUDP_TransceiverWithStub(port = 2121)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        udpBus.readBusUntilStopFlag(obj.helperMethod, arg, testKwarg='testKwarg')
        # Letting bus init before closing.
        # Otherwise, there is an issue that the message is not correctly being received.
        time.sleep(.0001)
        udpBus.stopFlag = True
        self.assertEqual(obj.message, self.testString)
        self.assertEqual(obj.args[0], arg)
        self.assertEqual(obj.testKwargs.get('testKwarg'), 'testKwarg')

    def test_readBusUntilStopFlagFail(self):
        obj = helperClass()
        udpBus = BusFactory.BusFactory.produceUDP_TransceiverWithStub(port = 2122)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        self.assertRaises(TypeError, udpBus.readBusUntilStopFlag, (obj.helperMethodNoArgs, arg), testKwarg='testKwarg')


if __name__ == '__main__':
    unittest.main()
