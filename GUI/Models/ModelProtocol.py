#!/usr/bin/env python3
# @author: Markus Kösters

from tkinter import Image
from typing import Protocol


class ModelProtocol(Protocol):
    """
    Class for prescribing the structure of the model.
    """

    def getFrame(self, frame: bytes) -> Image:
        """
        Method for receiving a single video frame.
        :return: Video frame as serialized numpy.ndarray.
        """
        pass
