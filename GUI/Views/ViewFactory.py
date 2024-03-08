#!/usr/bin/env python3
# @author: Markus Kösters
import tkinter

from .RootView import RootView
from .ViewConfigs import RootViewConfig


class ViewFactory:

    @staticmethod
    def produceRootView(window: tkinter.Tk):
        config = RootViewConfig(window, 'RobotGUI', '1920x1080')
        return RootView(config)
