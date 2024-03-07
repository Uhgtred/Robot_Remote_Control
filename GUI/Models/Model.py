#!/usr/bin/env python3
# @author: Markus Kösters

import joblib
import numpy

import Runners
from .ModelConfig import ModelConfig


class Model:

    def __init__(self, config: ModelConfig):
        self.__rawFrame = None
        self.__processedFrame = None
        self.__bus: config.bus = config.bus
        self.__imageFilePath: str = config.imageFilePath
        self.__runner: Runners = Runners.ThreadRunner()

    def getFrame(self):
        """
        Method for receiving a single video frame.
        :return: Video frame as serialized numpy.ndarray.
        """
        self.__runner.addTask(self.__receiveAndProcessNewFrame)
        self.__runner.runTasks()
        return self.__processedFrame

    def __receiveAndProcessNewFrame(self) -> None:
        """
        Method that controls how to receive and process new frames.
        """
        frame: bytes = self.__bus.readSingleMessage()
        self.__storeFrameinFile(frame, self.__imageFilePath)
        self.__processedFrame = self.__deserializeImageFile(self.__imageFilePath)

    def __deserializeImageFile(self, imageFilePath: str) -> numpy.ndarray:
        """
        Method for deserializing an image file.
        :param imageFilePath: File path of the image file that will be deserialized.
        """
        return joblib.load(imageFilePath)

    def __storeFrameinFile(self, imageData: bytes, imageFilePath: str) -> None:
        """
        Method to store the frame into a file.
        :param imageFilePath: Path in which the image will be stored.
        :param imageData: Data that will be stored in the file.
        """
        with open(imageFilePath, "wb") as file:
            file.write(imageData)
