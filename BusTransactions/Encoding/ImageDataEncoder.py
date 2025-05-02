import cv2
import numpy

import ProjectLogging
from BusTransactions.Encoding.EncodingProtocol import EncodingProtocol


class ImageDataEncoder(EncodingProtocol):

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('ImageDataEncoder',
                                                                      'ImageDataEncoder.log').getLogger

    @staticmethod
    def encode(imageData: numpy.ndarray) -> bytes:
        """
        Serialize raw image data into a compressed byte format.

        This function takes a NumPy ndarray representing image data, compresses it
        using JPEG encoding, and serializes it into a compact byte format using msgpack.
        The result includes the compressed image data in encoded byte array format,
        suitable for network transmission or storage.

        :param imageData: A NumPy ndarray containing raw image data to be serialized.
        :type imageData: numpy.ndarray
        :return: A serialized byte object containing the compressed image data in
            msgpack format.
        :rtype: Bytes
        """
        """ 
        Todo: This method does too much. It should be split into multiple methods. 
        It is currently not following the principle of single-responsibility.
        """
        ImageDataEncoder.__logger.debug(f'Serializing image data of type {type(imageData)} ...')
        # 80 is the quality of the jpeg compression.
        # This seems to be a good tradeoff between image-size and image-quality loss.
        encodingParameters: list[int] = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        ImageDataEncoder.__logger.debug(f'Encoding parameters: {encodingParameters}, imageDataType: {type(imageData)}')
        # returnValue is type boolean. This is not documented in cv2 docs.
        returnValue, buffer = cv2.imencode('.jpg', imageData, encodingParameters)
        return buffer.tobytes()

    @staticmethod
    def decode(data: bytes) -> any:
        """
        Decodes a given byte data utilizing msgpack unpacking and OpenCV decoding to
        obtain an image frame.

        This function processes serialized byte data (in msgpack format), unpacks it,
        extracts frame data, converts it into an array, and finally decodes the image
        data with OpenCV's imdecode function. The returned result is the image frame.

        :param data: Encoded byte data that contains serialized image frame information.
        :type data: bytes
        :return: Decoded image frame extracted from the provided byte data.
        :rtype: any
        """
        """ 
        Todo: This method does too much. It should be split into multiple methods. 
        It is currently not following the principle of single-responsibility.
        """
        ImageDataEncoder.__logger.debug(f'Image-data that will be decoded: {data}')
        frameData: numpy.ndarray = numpy.frombuffer(data, dtype=numpy.uint8)
        imageframe: numpy.ndarray = cv2.imdecode(frameData, cv2.IMREAD_COLOR)
        return imageframe