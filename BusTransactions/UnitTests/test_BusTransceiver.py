#!/usr/bin/env python3
# @author: Markus Kösters

import time
import unittest

from BusTransactions import DefaultBusFactory, BusPluginFactory
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
    message = None
    args = None
    testKwargs = None

    @classmethod
    def helperMethod(cls, message, *args, **kwargs):
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
        cls.args = list(args)
        if message == 'Hello World':
            cls.message = message
        cls.testKwargs = kwargs

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
    def setUp(self):
        self.testString = 'Hello World'

    def test_BusTransceiver_writeSingleMessage(self):
        serialTransceiver = DefaultBusFactory.DefaultBusFactory.produceSerialTransceiverWithStub()
        serialTransceiver.writeSingleMessage(self.testString)
        # intentionally not using the readSingleMessage, since this would rely on
        # the readSingleMessage for the test to run. But this test is about writing only.
        message = serialTransceiver.bus.serialBus.buffer.pop(0)[:-1].decode()
        self.assertEqual(message, self.testString)
        serialTransceiver.close()

    def test_BusTransceiver_readSingleMessage(self):
        serialTransceiver = DefaultBusFactory.DefaultBusFactory.produceSerialTransceiverWithStub()
        serialTransceiver.writeSingleMessage(self.testString)
        message = serialTransceiver.readSingleMessage()
        self.assertEqual(message, self.testString)
        serialTransceiver.close()

    def test_readBusUntilStopFlag(self):
        udpBus = DefaultBusFactory.DefaultBusFactory.produceUDP_TransceiverWithStub(2121)
        arg = 'testArg'
        udpBus.writeSingleMessage(self.testString)
        udpBus.readBusUntilStopFlag(helperClass.helperMethod, arg, testKwarg='testKwarg')
        # Letting bus init before closing.
        # Otherwise, there is an issue that the message is not correctly being received.
        time.sleep(.2)
        udpBus.stopFlag = True
        self.assertEqual(helperClass.message, self.testString)
        self.assertEqual(helperClass.args[0], arg)
        self.assertEqual(helperClass.testKwargs.get('testKwarg'), 'testKwarg')
        udpBus.close()

    def test_readBusUntilStopFlagFail(self):
        udpBus = DefaultBusFactory.DefaultBusFactory.produceUDP_TransceiverWithStub(2121)
        obj = helperClass()
        # udpBus = DefaultBusFactory.DefaultBusFactory.produceUDP_TransceiverWithStub(port = 2122)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        self.assertRaises(TypeError, udpBus.readBusUntilStopFlag, obj.helperMethodNoArgs, arg,
                          testKwarg='testKwarg')
        udpBus.close()

if __name__ == '__main__':
    unittest.main()
