#!/usr/bin/env python3
# @author: Markus Kösters

import tkinter

from .Models import ModelFactory
from .Models.ModelProtocol import ModelProtocol
from .Views import ViewFactory
from .Views.ViewProtocol import ViewProtocol


class GUI_Controller:

    __rootWindow = tkinter.Tk()
    __rootView: ViewProtocol = ViewFactory.produceRootView(__rootWindow)
    __rootModel: ModelProtocol = ModelFactory.produceRootModel()

    @classmethod
    def updateRootView(cls, frame: bytes) -> None:
        """
        Method that updates the view of the GUI based on the current model.
        """
        cls.__rootView.updateFrame(cls.__rootModel.getFrame(frame))
