#!/usr/bin/env python3
# @author: Markus Kösters

import tkinter
from tkinter import Image
from typing import Protocol


class ViewProtocol(Protocol):
    """
    Protocol for prescribing the structure of a View object.
    """

    def updateFrame(self, videoFrame: Image) -> None:
        """
        Protocol for prescribing the structure of an updateFrame-method.
        :param videoFrame:
        """