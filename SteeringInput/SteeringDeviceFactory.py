#!/usr/bin/env python3
# @author: Markus Kösters

from .SteeringDevice import SteeringDevice
from .SteeringDeviceConfig import SteeringDeviceConfig


class SteeringDeviceFactory:

    @staticmethod
    def produceController():
        config = SteeringDeviceConfig()
        return SteeringDevice(config).initController()
