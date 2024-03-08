#!/usr/bin/env python3
# @author: Markus Kösters

import tkinter
from tkinter import Image

from .ViewConfigs import RootViewConfig


class RootView:

    def __init__(self, config: RootViewConfig):
        self.__root = config.window
        self.__root.title(config.title)
        self.__root.geometry(config.geometry)
        self.videoLabel = self.__setVideoLabel()

    def updateFrame(self, videoFrame: Image) -> None:
        """
        Method for updating the video frame of the root window.
        :param videoFrame: Video frame that will be shown next.
        """
        # Update the label with new image
        self.videoLabel.config(image=videoFrame)
        self.videoLabel.image = videoFrame

    def __setVideoLabel(self) -> tkinter.Label:
        """
        Method for creating a video-label on the gui-window
        :return:
        """
        video_label = tkinter.Label(self.__root)
        video_label.pack()
        return video_label

