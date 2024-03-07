#!/usr/bin/env python3
# @author: Markus Kösters

import os.path
from pathlib import Path

from GUI.Models import Model
from .VideoControllerConfig import VideoControllerConfig
from .VideoControllerInterface import VideoControllerInterface


class VideoController(VideoControllerInterface):

    def __init__(self, config: VideoControllerConfig):
        self.__imageFilePath = str(Path(os.path.abspath(__file__)).parent) + config.filePath

    def processFrame(self, frame: bytes):
        Model(frame, self.__imageFilePath)





