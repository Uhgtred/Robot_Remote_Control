#!/usr/bin/env python3
# @author: Markus Kösters

import os.path
from pathlib import Path
import joblib
import numpy

from .VideoControllerConfig import VideoControllerConfig
from .VideoControllerInterface import VideoControllerInterface


class VideoController(VideoControllerInterface):

    def __init__(self, config: VideoControllerConfig):
        self.__imageFilePath = str(Path(os.path.abspath(__file__)).parent) + config.filePath

    def processFrame(self, frame: bytes):
        self.__storeFrameinFile(frame)
        frameData = self.__deserializeImageFile(self.__imageFilePath)
        # self.__updateModel(frameData)
        self.__updateView(frameData)

    def __updateView(self, frameData: numpy.ndarray) -> None:
        """
        Method for updating the GUI-view with the new image.
        :param frameData: Frame-data used to update the GUI-view.
        TODO: implement this!
        """
        pass

    def __deserializeImageFile(self, imageFilePath: str) -> numpy.ndarray:
        """
        Method for deserializing an image file.
        :param imageFilePath: File path of the image file that will be deserialized.
        """
        return joblib.load(imageFilePath)

    def __storeFrameinFile(self, imageData: bytes) -> None:
        """
        Method to store the frame into a file.
        :param imageData: Data that will be stored in the file.
        """
        with open(self.filePath, "wb") as file:
            file.write(imageData)
