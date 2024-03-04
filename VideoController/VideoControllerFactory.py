#!/usr/bin/env python3
# @author: Markus Kösters

from .VideoController import VideoController
from .VideoControllerConfig import VideoControllerConfig


class VideoControllerFactory:

    @staticmethod
    def produceVideoController() -> VideoController:
        config = VideoControllerConfig()
        return VideoController(config)
