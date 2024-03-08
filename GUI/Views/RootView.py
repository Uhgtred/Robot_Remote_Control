#!/usr/bin/env python3
# @author: Markus Kösters

import tkinter
from tkinter import Image

from .ViewConfigs import RootViewConfig


class RootView:

    def __init__(self, config: RootViewConfig):
        self.__root.title(config.title)
        self.__root.geometry(config.geometry)
        self.videoLabel = self.setVideoLabel()

    def updateFrame(self, videoFrame: Image):
        """
        TODO: Update GUI-Frame here with the new processed video frame!
        :param videoFrame:
        :return:
        """
        # Update the label with new image
        self.videoLabel.config(image=videoFrame)
        self.videoLabel.image = videoFrame

    def setVideoLabel(self) -> tkinter.Label:
        video_label = tkinter.Label(self.__root)
        video_label.pack()
        return video_label

