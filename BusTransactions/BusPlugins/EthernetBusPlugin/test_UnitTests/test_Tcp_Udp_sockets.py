#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions.BusPlugins.EthernetBusPlugin import SocketConfigs, Tcp_Udp_sockets
from . import SocketMock


class MyTestCase(unittest.TestCase):
    # print(MockBus)
    config = SocketConfigs.UdpSocketConfig('test.test.test.test', 4096, SocketMock.MockSocket)
    # print(config)
    bus = Tcp_Udp_sockets.UdpSocket(config)
    testString = b'Hello World'

    def test_write(self):
        self.bus.writeBus(self.testString)
        message = self.bus.sock.buffer.pop(0)
        assert message.endswith(self.testString)

    def test_read(self):
        self.bus.writeBus(self.testString)
        message = self.bus.readBus()
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
