#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import BusPluginFactory, BusPluginInterface


class TestUDPSockets(unittest.TestCase):
    """
    This class is a test case to validate the behavior and functionality of a
    bus plugin interface using UDP stub implementation.

    The purpose of this class is to test the read and write operations on the bus
    plugin by ensuring proper communication via the UDP protocol. It uses the
    BusPluginFactory to produce a plugin and simulates data transmission and
    reception for testing.

    :ivar bus: Instance of BusPluginInterface used to perform bus operations in
        the test cases.
    :type bus: BusPluginInterface
    :ivar testString: Byte string used to simulate data transmission and
        reception during the tests.
    :type testString: bytes
    """

    def setUp(self) -> None:
        self.bus: BusPluginInterface = BusPluginFactory.produceUdpStubPlugin(2333)
        self.testString = b'Hello World'

    def tearDown(self):
        self.bus.close()

    def test_write(self) -> None:
        """
        Tests the write functionality of the bus component by simulating a write
        operation to the bus, verifying that the message was written correctly
        to the socket buffer and checking the presence of expected content.

        :raises AssertionError: If the expected test string is not found in
            the message written to the socket buffer.
        """
        self.bus.writeBus(self.testString)
        message = self.bus.sock.buffer.pop(0)
        self.assertIn(self.testString, message)

    def test_read(self) -> None:
        """
        Tests the read functionality of the bus system to verify if the written
        message can be accurately read back. This ensures the integrity and
        correctness of message transmission in the bus system.

        :return: None
        """
        self.bus.writeBus(self.testString)
        message = self.bus.readBus()
        print(f'message: {message}')
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
