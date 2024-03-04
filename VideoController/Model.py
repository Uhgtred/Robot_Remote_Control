#!/usr/bin/env python3
# @author: Markus Kösters

import joblib
import numpy


class Model:

    def __init__(self, imageData: bytes, imageFilePath: str):
        self.__storeFrameinFile(imageData, imageFilePath)
        frameData = self.__deserializeImageFile(imageFilePath)
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

    def __storeFrameinFile(self, imageData: bytes, imageFilePath: str) -> None:
        """
        Method to store the frame into a file.
        :param imageData: Data that will be stored in the file.
        """
        with open(imageFilePath, "wb") as file:
            file.write(imageData)
