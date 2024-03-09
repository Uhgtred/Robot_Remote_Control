#!/usr/bin/env python3
# @author: Markus Kösters
import os.path
from pathlib import Path

import cv2
import joblib
import numpy
from PIL import ImageTk, Image

import Runners
from .ModelConfig import ModelConfig


class RootModel:

    def __init__(self, config: ModelConfig):
        self.__rawFrame: bytes = None
        self.__processedFrame: Image = None
        self.__imageFilePath: str = str(Path(os.path.abspath(__file__)).parent) + config.imageFilePath
        self.__runner: Runners = Runners.ThreadRunner()

    def getFrame(self, frame: bytes) -> Image:
        """
        Method for receiving a single video frame.
        :return: Video frame as serialized numpy.ndarray.
        """
        self.__runner.addTask(self.__receiveAndProcessNewFrame, frame)
        self.__runner.runTasks()
        return self.__processedFrame

    def __receiveAndProcessNewFrame(self, frame: bytes) -> None:
        """
        Method that controls how to receive and process new frames.
        """
        # Todo: bugfix this !!!
        self.__storeFrameinFile(frame, self.__imageFilePath)
        serializedFrame = self.__deserializeImageFile(self.__imageFilePath)
        self.__processedFrame = self.__converImageFormat(serializedFrame)

    def __deserializeImageFile(self, imageFilePath: str) -> numpy.ndarray:
        """
        Method for deserializing an image file.
        :param imageFilePath: File path of the image file that will be deserialized.
        """
        return joblib.load(imageFilePath)

    # Todo: check return-type
    def __converImageFormat(self, imageFrame: numpy.ndarray) -> Image:
        """
        Method for converting the image frame to a format that can be displayed in the GUI (tkinter).
        :param imageFrame: Serialized image frame that will be converted.
        :return:
        """
        return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)))

    def __storeFrameinFile(self, imageData: bytes, imageFilePath: str) -> None:
        """
        Method to store the frame into a file.
        :param imageFilePath: Path in which the image will be stored.
        :param imageData: Data that will be stored in the file.
        """
        with open(imageFilePath, "wb") as file:
            file.write(imageData)
