from typing import Protocol


class CompressionProtocol(Protocol):

    def compress(self, data: bytes) -> bytes:
        """
        Abstract method for compression of byte-data.
        :param data: Data that will be compressed
        :return: Compressed data
        """

    def deCompress(self, compressedData: bytes) -> bytes:
        """
        Abstract method for decompressing compressed byte-data.
        :param compressedData: Compressed Data that will be decompressed.
        :return: Decompressed data.
        """
