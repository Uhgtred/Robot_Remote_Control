#!/usr/bin/env python3
# @author: Markus Kösters

from .GuiConfig import GuiConfig


class GUI_Contoller:

    def __init__(self, config: GuiConfig):
        self.__model = config.model
        self.__view = config.view

    def updateGui(self) -> None:
        """
        Method that updates the view of the GUI based on the current model.
        """
        self.__view.updateFrame(self.__model.getFrame())
