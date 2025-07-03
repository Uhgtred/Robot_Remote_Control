import unittest

from BusTransactions import BusPluginFactory, AbstractBus
from BusTransactions.BusBuilder import BusBuilder
from BusTransactions.Compression.CompressorZlib import CompressorZlib
from BusTransactions.Encoding.PythonEncoder import PythonEncoder
from BusTransactions.Serialization.SerializerMsgPack import SerializerMsgPack


class TestBusBuilder(unittest.TestCase):

    def test_udpBusBuilder(self):
        plugin = BusPluginFactory.produceUdpStubPlugin(3434)
        builder = BusBuilder(plugin)
        print(builder.__class__.__name__)
        builder = builder.build()
        self.assertIsInstance(builder, AbstractBus)  # add assertion here

    def test_udpBusBuilderWithCompressor(self):
        plugin = BusPluginFactory.produceUdpStubPlugin(2413)
        builder = BusBuilder(plugin)
        compressor = CompressorZlib()
        builder = builder.setCompressor(compressor).build()
        self.assertIsInstance(builder._compressor, CompressorZlib)
        self.assertIsInstance(builder, AbstractBus)

    def test_udpBusBuilderWithSerializer(self):
        plugin = BusPluginFactory.produceUdpStubPlugin(1223)
        builder = BusBuilder(plugin)
        serializer = SerializerMsgPack()
        builder = builder.setSerializer(serializer).build()
        self.assertIsInstance(builder._serializer, SerializerMsgPack)
        self.assertIsInstance(builder, AbstractBus)

    def test_udpBusBuilderWithEncoder(self):
        plugin = BusPluginFactory.produceUdpStubPlugin(3438)
        builder = BusBuilder(plugin)
        encoder = PythonEncoder()
        builder = builder.setEncoder(encoder).build()
        self.assertIsInstance(builder._encoder, PythonEncoder)
        self.assertIsInstance(builder, AbstractBus)

    def test_udpBusBuilderWithAllOptions(self):
        plugin = BusPluginFactory.produceUdpStubPlugin(3430)
        builder = BusBuilder(plugin)
        encoder = PythonEncoder()
        compressor = CompressorZlib()
        serializer = SerializerMsgPack()
        builder = (builder
                    .setEncoder(encoder)
                    .setCompressor(compressor)
                    .setSerializer(serializer)
                    .build())
        self.assertIsInstance(builder._encoder, PythonEncoder)
        self.assertIsInstance(builder._compressor, CompressorZlib)
        self.assertIsInstance(builder._serializer, SerializerMsgPack)
        self.assertIsInstance(builder, AbstractBus)

if __name__ == '__main__':
    unittest.main()
