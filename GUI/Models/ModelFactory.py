#!/usr/bin/env python3
# @author: Markus Kösters

import BusTransactions.BusFactory
from .RootModel import RootModel
from .ModelConfig import ModelConfig


class ModelFactory:

    @staticmethod
    def produceRootModel():
        config = ModelConfig()
        return RootModel(config=config)
