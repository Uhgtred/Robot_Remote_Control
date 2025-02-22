#!/usr/bin/env python3
# @author: Markus Kösters

from .SteeringDevice import SteeringDevice
from .SteeringDeviceConfig import SteeringDeviceConfig


class SteeringDeviceFactory:

    @staticmethod
    def produceController() -> SteeringDevice:
        """
        Produces and initializes a SteeringDevice instance with the
        necessary configuration. The function creates a configuration
        object for a steering device, uses it to instantiate the device,
        and initializes its controller before returning the ready-to-use
        SteeringDevice instance.

        :rtype: SteeringDevice
        :return: A fully initialized SteeringDevice instance ready for use
                 with its controller.
        """
        config = SteeringDeviceConfig()
        steeringDevice = SteeringDevice(config)
        steeringDevice.initController()
        return steeringDevice
