#!/usr/bin/env python3
# @author: Markus Kösters

from .ModelConfig import ModelConfig
from .RootModel import RootModel


class ModelFactory:

    @staticmethod
    def produceRootModel1920x1080() -> RootModel:
        """
        Factory-method creating a RootModel-Object with a resolution of 1920x1080 Pixels.
        :return: RootModel
        """
        config = ModelConfig(resolution=[1920, 1080])
        return RootModel(config=config)
