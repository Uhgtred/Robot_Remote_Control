#!/usr/bin/env python3
# @author   Markus Kösters

import logging
import os.path


class Logger:
    """
    Class for logging. The logfiles will be created inside the "ProjectLogging"-package by default.

    This class provides a centralized logging mechanism for the application. It supports both
    file and console logging with customizable log levels. Old log files are automatically
    deleted when the class is loaded to prevent storage issues.

    Console-logs are activated by default and can be deactivated by passing "consoleOutput = False" to the instance.
    This class has to be instanced BEFORE calling the "getLogger" property.

    Attributes
    ----------
    __logger : logging.Logger
        The internal logger instance used for logging

    Examples
    --------
    >>> logger = Logger('MyComponent', 'component.log').getLogger
    >>> logger.info('This is an information message')
    >>> logger.error('An error occurred')
    """

    def __init__(self, name: str, logFile: str = './MainLog.log', logLevel: int = logging.DEBUG, consoleOutput: bool = True):
        """
        Initialize a new Logger instance with specified configuration.

        This constructor sets up the logger with the specified name, log file, log level, and console output settings.
        It automatically adds the '.log' extension to the log file name if not present.

        Parameters
        ----------
        name : str
            Name of the logger, used to identify the source of log messages
        logFile : str, optional
            Name of the log file (default is './MainLog.log')
        logLevel : int, optional
            Level of the logs (default is logging.DEBUG)
        consoleOutput : bool, optional
            Whether to output logs to the console (default is True)
        """
        if not logFile.endswith('.log'):
            logFile += '.log'
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logLevel)
        formatter: logging.Formatter = self.__setupFormatter(name)
        self.__setupFileHandler(logLevel, logFile, formatter, self.__logger)
        if consoleOutput:
            self.__setupConsoleHandler(logLevel, formatter, self.__logger)

    @staticmethod
    def __setupConsoleHandler(loglevel: int, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Set up a console log handler for displaying log messages in the console.

        This method creates and configures a StreamHandler that outputs log messages to the console
        with the specified log level and formatting.

        Parameters
        ----------
        loglevel : int
            The minimum log level for messages to be displayed in the console
        formatter : logging.Formatter
            The formatter that defines the style and format of log messages
        logger : logging.Logger
            The logger instance to which the console handler will be attached

        Returns
        -------
        None
        """
        consoleHandler: logging.StreamHandler = logging.StreamHandler()
        consoleHandler.setLevel(loglevel)  # Only log INFO and above to the console
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

    @staticmethod
    def __setupFileHandler(logLevel: int, logFile: str, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Set up a file handler for writing log messages to a file.

        This method creates and configures a FileHandler that writes log messages to the specified file
        with the specified log level and formatting. The log file is created in the ProjectLogging directory.

        Parameters
        ----------
        logLevel : int
            The minimum log level for messages to be written to the log file
        logFile : str
            The name of the log file. Base path is the "ProjectLogging" package
        formatter : logging.Formatter
            The formatter that defines the style and format of log messages
        logger : logging.Logger
            The logger instance to which the file handler will be attached

        Returns
        -------
        None
        """
        fileHandler: logging.FileHandler = logging.FileHandler(os.path.join(os.path.dirname(__file__), logFile))
        fileHandler.setLevel(logLevel)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    @staticmethod
    def __setupFormatter(name: str) -> logging.Formatter:
        """
        Create and configure a formatter for log messages.

        This method defines the format of log messages, including timestamp, log level, 
        logger name, and the actual message content.

        Parameters
        ----------
        name : str
            The name of the logger, used in the formatted log message

        Returns
        -------
        logging.Formatter
            A configured formatter object that will be used to format log messages
        """
        return logging.Formatter('%(asctime)s - [%(levelname)s][%(name)s]: %(message)s\t',
                                 datefmt='%d-%m-%Y %H:%M:%S')

    @property
    def getLogger(self):
        """
        Get the configured logger instance.

        This property provides access to the internal logger instance that has been configured
        with the specified handlers and formatters. The returned logger can be used to create
        log messages at various levels (debug, info, warning, error, critical).

        Returns
        -------
        logging.Logger
            The configured logger instance that can be used to create file and console logs
        """
        return self.__logger

    @staticmethod
    def __deleteExistingLogFiles() -> None:
        """
        Delete all existing log files in the ProjectLogging directory.

        This method is automatically called when the Logger class is loaded by the interpreter.
        It ensures that old log data doesn't accumulate and waste storage space. All files with
        the '.log' extension in the same directory as this module will be removed.

        Returns
        -------
        None
        """
        logPath = os.path.dirname(__file__)
        files = os.listdir(logPath)
        for file in files:
            if file.endswith('.log'):
                os.remove(os.path.join(logPath, file))

    """
    Executing the deletion of existing logfiles ones the class is being created by the interpreter.
    This ensures that no old log-data is polluting the logs and the storage is not being flooded with log-data.
    """
    __deleteExistingLogFiles()
