#!/usr/bin/env python3
# @author: Markus Kösters

from .Controller import Controller
from .ControllerConfig import ControllerConfig


class ControllerFactory:

    @staticmethod
    def produceController():
        config = ControllerConfig()
        return Controller(config)