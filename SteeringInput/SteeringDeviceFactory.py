#!/usr/bin/env python3
# @author: Markus Kösters
import ProjectLogging
from .SteeringDevice import SteeringDevice
from .SteeringDeviceConfig import SteeringDeviceConfig


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


    @staticmethod
    def produceControllerStub(stubObject: type(SteeringDevice)) -> SteeringDevice:
        """
        Produces a controller stub using the provided SteeringDevice class. This method
        creates a configuration object of type SteeringDeviceConfig, initializes the
        provided SteeringDevice class with the configuration, and returns the resulting
        instance.

        :param stubObject: A class of type SteeringDevice used to produce the controller stub.
        :return: An instance of SteeringDevice initialized with a SteeringDeviceConfig.
        """
        config = SteeringDeviceConfig()
        steeringDevice = stubObject(config)
        SteeringDeviceFactory._SteeringDeviceFactory__logger.debug(f"SteeringDevice stub created: {steeringDevice}")
        return steeringDevice
