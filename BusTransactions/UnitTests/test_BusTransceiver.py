#!/usr/bin/env python3
# @author: Markus Kösters

import logging
import time
import unittest

from BusTransactions import Encoding, BusPluginFactory
from BusTransactions.BusFactory import BusFactory


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

    args = None
    message = None
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
        cls.message = message
        cls.testKwargs = kwargs

    @classmethod
    def helperMethodNoArgs(cls):
        """
        This method is a placeholder that performs no operation. It is intended to
        test whether an exception is raised during unit testing, due to a missing argument of this method
        or other validation processes.

        :return: None
        """
        # does not need to do anything since this is only used
        # to check wether the exception is being raised
        pass


class test_BusTransceiver(unittest.TestCase):
    bus = BusPluginFactory.produceSerialBusStubPlugin()
    serialTransceiver = BusFactory.produceCustomBusTransceiver(bus, Encoding.EncodingFactory.arduinoSerialEncoding)
    testString = 'Hello World'
    messages = []
    __logger: logging.Logger = logging.getLogger(__name__)

    def test_BusTransceiver_writeSingleMessage(self):
        serialTransceiver = BusFactory.produceSer()
        self.serialTransceiver.writeSingleMessage(self.testString)
        message = self.serialTransceiver.bus.bus.buffer.pop(0)
        self.assertEqual(message[:-1], self.testString.encode())

    def test_BusTransceiver_readSingleMessage(self):
        self.serialTransceiver.writeSingleMessage(self.testString)
        message = self.serialTransceiver.readSingleMessage()
        self.assertEqual(message, self.testString)

    def test_readBusUntilStopFlag(self):
        obj = helperClass()
        udpBus = BusFactory.produceUDP_TransceiverWithStub(port = 2121)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        udpBus.readBusUntilStopFlag(obj.helperMethod, arg, testKwarg='testKwarg')
        # Letting bus init before closing.
        # Otherwise, there is an issue that the message is not correctly being received.
        time.sleep(.0001)
        udpBus.stopFlag = True
        self.__logger.debug(f'Message that has been read from the socket-mock: {obj.message}')
        self.assertEqual(obj.message, self.testString)
        self.assertEqual(obj.args[0], arg)
        self.assertEqual(obj.testKwargs.get('testKwarg'), 'testKwarg')

    def test_readBusUntilStopFlagFail(self):
        obj = helperClass()
        udpBus = BusFactory.produceUDP_TransceiverWithStub(port = 2122)
        udpBus.writeSingleMessage(self.testString)
        arg = 'testArg'
        self.assertRaises(TypeError, udpBus.readBusUntilStopFlag, (obj.helperMethodNoArgs, arg), testKwarg='testKwarg')


if __name__ == '__main__':
    unittest.main()
