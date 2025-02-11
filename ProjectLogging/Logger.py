#!/usr/bin/env python3
# @author   Markus Kösters

import logging
import os.path


class Logger:
    """
    Class for logging. The logfiles will be created inside the "ProjectLogging"-package by default.
    Console-logs are activated by default and can be deactivated by passing "consoleOutput = False" to the instance.
    This class has to be instanced BEFORE calling the "getLogger" property.
    """

    def __init__(self, name: str, logFile: str = './MainLog.log', logLevel: int = logging.INFO, consoleOutput: bool = True):
        if not logFile.endswith('.log'):
            logFile += '.log'
        self.__deleteExistingLogFiles()
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logLevel)
        formatter: logging.Formatter = self.__setupFormatter(name)
        self.__setupFileHandler(logLevel, logFile, formatter, self.__logger)
        if consoleOutput:
            self.__setupConsoleHandler(logLevel, formatter, self.__logger)

    @staticmethod
    def __setupConsoleHandler(loglevel: int, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Method for setting up a console-log-handler.
        :param loglevel: Defines which log messages shall be streamed to the console.
        :param formatter: Defines the style of the log-messages in the console.
        :param logger: The logger that this console-streamer is being attached to.
        """
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(loglevel)  # Only log INFO and above to the console
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

    @staticmethod
    def __setupFileHandler(logLevel: int, logFile: str, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Method for creating a file-handler for the logging.
        :param logLevel: Defines which log messages shall be stored into the log-file.
        :param formatter: Defines the style of the log-messages in the log-file.
        :param logFile: The log-file that the logs shall be stored in. Base-path is the "ProjectLogging" package.
        """
        fileHandler = logging.FileHandler(os.path.join(os.path.dirname(__file__), logFile))
        fileHandler.setLevel(logLevel)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    @staticmethod
    def __setupFormatter(name: str) -> logging.Formatter:
        """
        Method defining the format of the logs.
        :return: Formatter, that will be used to set up the style of the logging.
        """
        return logging.Formatter('%(asctime)s - [%(levelname)s][%(name)s]: %(message)s\t',
                                 datefmt='%d-%m-%Y %H:%M:%S')

    @property
    def getLogger(self):
        """
        Getter for the Logger-instance.
        :return: Logger that can be used to create file-logs and console-logs (can be deactivated while instancing).
        """
        return self.__logger

    @staticmethod
    def __deleteExistingLogFiles() -> None:
        """
        Method for deleting old logs. So they do not stack up and waste memory.
        """
        logPath = os.path.dirname(__file__)
        files = os.listdir(logPath)
        for file in files:
            if file.endswith('.log'):
                os.remove(os.path.join(logPath, file))
