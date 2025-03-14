#!/usr/bin/env python3
# @author: Markus Kösters
import ProjectLogging
from .SteeringDevice import SteeringDevice
from .SteeringDeviceConfig import SteeringDeviceConfig
from .UnitTests.SteeringDeviceStub import SteeringDeviceStub


class SteeringDeviceFactory:

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('SteeringDeviceFactory',
                                                                      'SteeringDeviceFactory.log').getLogger

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

    @staticmethod
    def produceControllerWithoutInitOfController() -> SteeringDevice:
        """
        Produces and initializes a SteeringDevice instance with the
        necessary configuration. The function creates a configuration
        object for a steering device, uses it to instantiate the device
        and return a SteeringDevice instance without an initialized controller.

        :rtype: SteeringDevice
        :return: A fully initialized SteeringDevice instance ready for use
                 with its controller.
        """
        config = SteeringDeviceConfig()
        steeringDevice = SteeringDevice(config)
        return steeringDevice
