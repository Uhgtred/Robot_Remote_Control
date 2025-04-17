import zlib

from BusTransactions.Compression.CompressionProtocol import CompressionProtocol


class CompressorZlib(CompressionProtocol):

    def compress(self, data: bytes) -> bytes:
        """
        Method for compressing data using zlib library.
        :param data:
        :return:
        """
        return zlib.compress(data)

    def deCompress(self, compressedData: bytes) -> bytes:
        """
        Method for decompressing data using zlib library.
        :param compressedData:
        :return:
        """
        return zlib.decompress(compressedData)

