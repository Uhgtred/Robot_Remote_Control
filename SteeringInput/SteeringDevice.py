#!/usr/bin/env python3
# @author   Markus Kösters

import subprocess
from dataclasses import fields
import evdev

from .SteeringDeviceConfig import SteeringDeviceConfig, ButtonData, ButtonsInterface


class SteeringDevice:
    """
    A class implementing a steering device interface, its configurations, and interactions.

    This class allows interaction with a configured steering device by detecting and
    connecting the controller, processing inputs, and executing callback methods for
    controller events. It integrates with the `ButtonsInterface` object specified in
    `ControllerConfig`, providing the ability to map input events to steering-device
    values. This implementation is primarily designed to function on Linux systems.

    :ivar __conf: Configuration object containing settings specific to the steering device.
    :type __conf: SteeringDeviceConfig
    :ivar __controller: Represents the connected controller device or None if uninitialized.
    :type __controller: Optional[evdev.InputDevice]
    """

    def __init__(self, config: SteeringDeviceConfig):
        self.__conf = config
        self.__controller = None

    def __setSteeringValues(self, event: evdev.InputEvent) -> ButtonsInterface:
        """
        Sets the steering values based on the event received and updates the button
        configuration.

        This method traverses through the configurable button fields, matches the event
        code with the button ID, and updates the button value if a match is found.

        :param event: Input event containing the code and value used to update the
                      button configuration.
        :type event: evdev.InputEvent
        :return: Updated buttons configuration with modified button values based on
                 the received event.
        :rtype: ButtonsInterface
        """
        for field in fields(self.__conf.buttons):
            # getting the content of each field
            fieldContent = getattr(self.__conf.buttons, field.name)
            if not isinstance(fieldContent, ButtonData):
                continue
            if fieldContent.ID == event.code:
                fieldContent.value = event.value
        return self.__conf.buttons

    def initController(self, vendor: int = None) -> None:
        """
        Initializes the controller for the device with the specified vendor ID. If no vendor ID is specified,
        a default one is used from the configuration. Searches for available devices in the configured
        controller path, validates the vendor ID, and sets an appropriate device as the controller.

        :param vendor: The vendor ID of the controller. If not provided, defaults to
                       the value in the configuration.
        :type vendor: int
        :raises TypeError: If no compatible device matching the given vendor ID is found.
        :return: None
        """
        if not vendor:
            vendor: int = self.__conf.DeviceVendorID
        path: str = self.__conf.ControllerPath
        deviceList: list = self.__searchAvailableDevices(path)
        # Checking if a device meets the given vendor-id. If so, set it as the controller.
        result:bool = False
        for device in deviceList:
            device = f'{path}{device}'
            if 'event' not in device:
                continue
            # setting the device to a file of the input-directory
            device = evdev.InputDevice(device)
            result:bool = self.__checkVendorID(device, vendor)
            if result:
                break
        if not result:
            raise TypeError(f'SteeringInput not found! ID provided: {vendor}')

    def __checkVendorID(self, device: evdev.InputDevice, vendor: int) -> bool:
        """
        Checks if the given device matches the specified vendor ID and updates the
        controller attribute with the device if the match is successful.

        :param device: The input device to be checked.
        :type device: evdev.InputDevice
        :param vendor: The vendor ID to be checked against the device's vendor ID.
        :type vendor: int
        :return: A boolean indicating whether the device's vendor ID matches the
                 specified vendor ID.
        :rtype: bool
        """
        if device.info.vendor == vendor:
            self.__controller = device
            return True
        return False

    def __searchAvailableDevices(self, path: str) -> list:
        """
        Searches for available devices in a given directory path by listing all items
        in the directory. This function utilizes the `ls` command to fetch the
        directory contents and processes the result into a list of device names.

        :param path: The directory path to search for available devices. Should be a
            valid string representing a directory path on the filesystem.
        :type path: str
        :return: A list of device names found in the specified directory. If the
            directory is empty, the returned list will be empty.
        :rtype: list
        """
        directoryListing = subprocess.Popen(['ls', path], stdout=subprocess.PIPE).communicate()
        return (directoryListing[0]).decode().strip().split('\n')

    def readController(self, callbackMethod: callable) -> None:
        """
        Reads input events from the controller and processes them using the provided
        callback method. This function ensures that the controller is exclusively
        accessed by the current code, processes each event from the controller,
        and skips events of type 0. Steering values corresponding to each valid
        event are passed to the callback method for further handling.

        :param callbackMethod: A callable that processes steering values derived
            from controller events.
        :return: None
        :raises BaseException: If no controller has been initialized.
        """
        if not self.__controller:
            raise BaseException('No controller has been initialized!')
        self.__controller.grab()  # makes the controller only listen to this Code
        for event in self.__controller.read_loop():
            if event.type == 0:
                continue
            callbackMethod(self.__setSteeringValues(event).getButtonDict)
