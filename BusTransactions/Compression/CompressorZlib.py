import zlib

from BusTransactions.Compression.CompressorInterface import CompressorInterface


class CompressorZlib(CompressorInterface):

    def compress(self, data: bytes) -> bytes:
        """
        Method for compressing data using zlib.
        :param data:
        :return:
        """
        return zlib.compress(data)

    def deCompress(self, compressedData: bytes) -> bytes:
        """
        Method for decompressing data using zlib.
        :param compressedData:
        :return:
        """
        return zlib.decompress(compressedData)

