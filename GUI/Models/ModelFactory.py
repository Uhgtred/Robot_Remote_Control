#!/usr/bin/env python3
# @author: Markus Kösters

import BusTransactions.BusFactory
from .Model import Model
from .ModelConfig import ModelConfig


class ModelFactory:

    @staticmethod
    def produceModel():
        bus = BusTransactions.BusFactory.BusFactory.produceUDP_Transceiver(host=False, port=2002)
        config = ModelConfig(bus=bus)
        return Model(config=config)
