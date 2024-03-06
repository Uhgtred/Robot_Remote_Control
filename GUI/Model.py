#!/usr/bin/env python3
# @author: Markus Kösters

import joblib
import numpy

import Runners
from BusTransactions.BusFactory import BusFactory


class Model:
    def __init__(self):
        self._data = None

    def store_data(self, data):
        self._data = data

    def retrieve_data(self):
        return self._data

class Model:

    def __init__(self, config: ModelConfig):
        self.__rawFrame = None
        self.__storeFrameinFile(imageData, imageFilePath)
        frameData = self.__deserializeImageFile(imageFilePath)
        # self.__updateModel(frameData)
        self.__updateView(frameData)
        self.__bus = BusFactory.produceUDP_Transceiver(host=False, port=config.port)
        self.__runner = Runners.ThreadRunner()

    def getFrame(self):
        """
        Method for receiving a single video frame.
        :return: Video frame as serialized numpy.ndarray.
        """
        self.__runner.addTask(self.__receiveAndProcessNewFrame)
        self.__runner.runTasks()
        return self.__processedFrame

    def __receiveAndProcessNewFrame(self):
        frame = self.__bus.readSingleMessage()
        self.storeFrameinFile(frame, self)

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

    def storeFrameinFile(self, imageData: bytes, imageFilePath: str) -> None:
        """
        Method to store the frame into a file.
        :param imageData: Data that will be stored in the file.
        """
        with open(imageFilePath, "wb") as file:
            file.write(imageData)
