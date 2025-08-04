import inspect
from abc import ABC
from inspect import Signature

import ProjectLogging
import Runners
from BusTransactions.BusPlugins.BusPluginInterface import BusPluginInterface
from BusTransactions.Compression.CompressionProtocol import CompressionProtocol
from BusTransactions.Encoding import EncodingProtocol
from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class AbstractBus(ABC):
    """
    A flexible communication interface for various bus systems.

    This class provides a unified interface for communicating with different bus systems
    (like UDP, Serial, etc.) through plugins. It supports reading and writing messages,
    with optional processing steps including compression, serialization, and encoding/decoding.

    The Bus class can operate in two modes:
    1. Single message mode - for one-time reads/writes
    2. Continuous reading mode - for reading messages in a loop until stopped

    Attributes
    ----------
    bus : AbstractBusPlugin
        The underlying bus plugin that handles the actual communication
    _compressor : CompressionProtocol | None
        Optional component for compressing/decompressing messages
    _serializer : SerializationProtocol | None
        Optional component for serializing/deserializing messages
    _encoder : EncodingProtocol | None
        Optional component for encoding/decoding messages
    _stopFlag : bool
        Flag to control continuous reading loops
    """

    __logger: ProjectLogging.Logger.getLogger or None = None

    def __init__(self, busPlugin: BusPluginInterface) -> None:
        """
        Initialize a new Bus instance with the specified bus plugin.

        This constructor sets up the Bus instance with the provided bus plugin and initializes
        internal state variables for compression, serialization, and encoding.

        Parameters
        ----------
        busPlugin : AbstractBusPlugin
            The bus plugin that will handle the actual communication.
            Must implement the AbstractBusPlugin interface.
        """
        self.__logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Bus', 'Bus.log').getLogger
        self.__logger.info(f'Creating a Bus-instance with plugin: {busPlugin}')
        self._stopFlag: bool = False
        self.bus: BusPluginInterface = busPlugin
        self._compressor: CompressionProtocol | None = None
        self._serializer: SerializationProtocol | None = None
        self._encoder: EncodingProtocol | None = None
        self.__threadRunner: Runners.ThreadRunner = Runners.ThreadRunner()

    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and process a single message from the bus.

        This method reads a single message from the underlying bus plugin, then applies
        any configured post-processing steps (decompression, deserialization, decoding)
        before returning the message.

        Returns
        -------
        any
            The decoded message from the bus. The exact type depends on the configured
            encoder, or bytes if no encoder is set.

        Raises
        ------
        BaseException
            If an error occurs while reading from the bus
        """
        self.__logger.debug(f'Reading message from bus: {self.bus.__class__.__name__}')
        try:
            message: bytes = self.bus.readBus()
        except Exception as exception:
            self.__logger.debug(f'Error while trying to read a message from the bus: {exception}')
            raise BaseException(f'Error while trying to read a message from the bus: {exception}')
        message: str = self._postProcessMessageFromReceiving(message)
        self.__logger.debug(f'Message that has been received: {message}')
        return message

    def readBusUntilStopFlag(self, callbackMethod: callable, *args, **kwargs) -> None:
        """
        Read messages from the bus continuously until the stop flag is set.

        This method starts a new thread that continuously reads messages from the bus
        and passes them to the provided callback method. The reading loop continues
        until the stop flag is set to True using the stopFlag property.

        Parameters
        ----------
        callbackMethod : callable
            Method that will be called with each received message. Must accept at least
            one argument which will be the message read from the bus.
        *args
            Additional positional arguments to pass to the callback method
        **kwargs
            Additional keyword arguments to pass to the callback method

        Raises
        ------
        TypeError
            If the callback method is not callable or doesn't accept at least one argument
        """
        self._callBackHasInputArg(callbackMethod)
        self.__threadRunner.addTask(self._readLoop, *[callbackMethod, *args], **kwargs)
        self.__threadRunner.runTasks()

    def _readLoop(self, callbackMethod: callable, *args, **kwargs) -> None:
        """
        Internal method that implements the continuous reading loop.

        This method contains the logic to repeatedly read messages from the bus and
        pass them to the callback method until the stop flag is set to True. It handles
        exceptions that might occur during reading or callback execution to prevent
        the loop from terminating unexpectedly.

        Parameters
        ----------
        callbackMethod : callable
            Method that will be called with each received message
        *args
            Additional positional arguments to pass to the callback method
        **kwargs
            Additional keyword arguments to pass to the callback method

        Returns
        -------
        None
        """
        while not self._stopFlag:
            try:
                self.__logger.debug(f'Trying to read a message with callback-method '
                                    f'[{self.readSingleMessage.__name__}]\n'
                                    f'\twith args: {args}\n'
                                    f'\tand kwargs: {kwargs}\n'
                                    f'\ton bus: {self.bus.__class__.__name__}')
                message: any = self.readSingleMessage()
                self.__logger.debug(f'Message received: {message}')
                callbackMethod(message, *args, **kwargs)
            except Exception as e:
                self.__logger.error(f'Error while reading message: {e}')

    @staticmethod
    def _callBackHasInputArg(callbackMethod: callable) -> None:
        """
        Validate that the provided callback method meets the required interface.

        This method checks that the callback method is callable and accepts at least
        one input argument, which is necessary to receive the message from the bus.

        Parameters
        ----------
        callbackMethod : callable
            The callback method to validate

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the callback method is not callable or doesn't accept at least one argument
        """
        # Checking if the method is callable. Else raising an error.
        if callable(callbackMethod):
            signature: Signature = inspect.signature(callbackMethod)
            # Checking if the method accepts at least one argument. Else raising an error.
            if len(signature.parameters) < 1:
                raise TypeError("Callback-method is not accepting any input-arguments."
                                "At least one input-argument.")
        else:
            raise TypeError("Callback-method is not callable.")

    def writeSingleMessage(self, message: any) -> None:
        """
        Send a single message to the bus with pre-processing.

        This method applies any configured pre-processing steps (encoding, serialization,
        compression) to the message before sending it to the underlying bus plugin.

        Parameters
        ----------
        message : any
            The message to send. The type can be any that is supported by the
            configured encoder, or bytes if no encoder is set.

        Returns
        -------
        None

        Raises
        ------
        BaseException
            If an error occurs while sending the message to the bus
        """
        self.__logger.debug(f'Sending message: "{message}" to bus: [{self.bus.__class__.__name__}]')
        message: bytes = self._preProcessMessageForTransmission(message)
        try:
            self.bus.writeBus(message)
        except Exception as exception:
            self.__logger.debug(f'Error while trying to send a message to the bus: {exception}!')
            raise BaseException(f'Error while trying to send a message to the bus: {exception}!')

    def _preProcessMessageForTransmission(self, message: any) -> bytes:
        """
        Apply pre-processing steps to a message before transmission.

        This internal method applies the configured processing steps to prepare a message
        for transmission. The steps are applied in a specific order:
        1. Encoding - Convert the message to a standard format
        2. Serialization - Convert the encoded message to a serialized format
        3. Compression - Compress the serialized message to reduce size

        Parameters
        ----------
        message : any
            The original message to process

        Returns
        -------
        bytes
            The processed message ready for transmission
        """
        # The order is important for the following methods.
        message: bytes = self._encode(message)
        message: bytes = self._serialize(message)
        message: bytes = self._compress(message)
        return message

    def _postProcessMessageFromReceiving(self, message: bytes) -> str:
        """
        Apply post-processing steps to a received message.

        This internal method applies the configured processing steps to a received message
        to convert it back to its original form. The steps are applied in a specific order:
        1. Decompression - Decompress the message if it was compressed
        2. Deserialization - Convert the message from serialized format
        3. Decoding - Convert the message to its final format

        Parameters
        ----------
        message : bytes
            The raw message received from the bus

        Returns
        -------
        any
            The processed message in its original form. The exact type depends on
            the configured decoder.
        """
        # The order is important for the following methods.
        message: bytes = self._deCompress(message)
        message: bytes = self._deSerialize(message)
        message: str = self._decode(message)
        return message

    def close(self) -> None:
        """
        Close the underlying bus connection.

        This method closes the connection to the bus by calling the close method
        of the underlying bus plugin. It should be called when the bus is no longer
        needed to release any resources held by the bus plugin.

        Returns
        -------
        None
        """
        try:
            self.__logger.info(f'Closing bus [{self.bus}]!')
            self.bus.close()
        except Exception as exception:
            self.__logger.warning(f'Bus [{self.bus}] could not be closed properly! Original exception: {exception}')

    @property
    def stopFlag(self) -> bool:
        """
        Get the current state of the stop flag.

        This property provides access to the internal stop flag that controls
        continuous reading loops. When set to True, any active reading loops
        will terminate after their current iteration.

        Returns
        -------
        bool
            The current state of the stop flag
        """
        return self._stopFlag

    @stopFlag.setter
    def stopFlag(self, state: bool) -> None:
        """
        Set the state of the stop flag.

        This setter allows changing the state of the internal stop flag. Setting it to True
        will cause any active reading loops to terminate after their current iteration.
        Setting it to False allows new reading loops to be started.

        Parameters
        ----------
        state : bool
            The new state for the stop flag

        Returns
        -------
        None
        """
        self._stopFlag: bool = state
        self.close()

    def _compress(self, data: bytes) -> bytes:
        """
        Compress data before sending it via the bus.

        This internal method applies compression to the data if a compressor is configured.
        If no compressor is set, the data is returned unchanged.

        Parameters
        ----------
        data : bytes
            The data to compress

        Returns
        -------
        bytes
            The compressed data if a compressor is set, otherwise the original data
        """
        return self._compressor.compress(data) if self._compressor else data

    def _deCompress(self, data: bytes) -> bytes:
        """
        Decompress data received from the bus.

        This internal method applies decompression to the data if a compressor is configured.
        If no compressor is set, the data is returned unchanged.

        Parameters
        ----------
        data : bytes
            The compressed data to decompress

        Returns
        -------
        bytes
            The decompressed data if a compressor is set, otherwise the original data
        """
        return self._compressor.deCompress(data) if self._compressor else data

    def _encode(self, data: any) -> bytes:
        """
        Encode data before sending it via the bus.

        This internal method applies encoding to the data if an encoder is configured.
        If no encoder is set, the data is returned unchanged.

        Parameters
        ----------
        data : any
            The data to encode

        Returns
        -------
        bytes
            The encoded data if an encoder is set, otherwise the original data
        """
        return self._encoder.encode(data) if self._encoder else data

    def _decode(self, data: bytes) -> any:
        """
        Decode data received from the bus.

        This internal method applies decoding to the data if an encoder is configured.
        If no encoder is set, the data is returned unchanged.

        Parameters
        ----------
        data : bytes
            The encoded data to decode

        Returns
        -------
        any
            The decoded data if an encoder is set, otherwise the original data.
            The exact return type depends on the configured encoder.
        """
        return self._encoder.decode(data) if self._encoder else data

    def _serialize(self, data: any) -> bytes:
        """
        Serialize data before sending it via the bus.

        This internal method applies serialization to the data if a serializer is configured.
        If no serializer is set, the data is returned unchanged.

        Parameters
        ----------
        data : any
            The data to serialize

        Returns
        -------
        bytes
            The serialized data if a serializer is set, otherwise the original data
        """
        return self._serializer.serialize(data) if self._serializer else data

    def _deSerialize(self, data: bytes) -> any:
        """
        Deserialize data received from the bus.

        This internal method applies deserialization to the data if a serializer is configured.
        If no serializer is set, the data is returned unchanged.

        Parameters
        ----------
        data : bytes
            The serialized data to deserialize

        Returns
        -------
        any
            The deserialized data if a serializer is set, otherwise the original data.
            The exact return type depends on the configured serializer.
        """
        return self._serializer.deSerialize(data) if self._serializer else data
