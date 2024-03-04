#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class VideoControllerInterface(ABC):

    @abstractmethod
    def processFrame(self, frame: bytes) -> None:
        """
        Interface for processing video frames.
        :param frame: Serialized frame that will be processed (in bytes format).
        """
