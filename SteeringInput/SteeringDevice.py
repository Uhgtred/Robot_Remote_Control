#!/usr/bin/env python3
# @author   Markus Kösters

import subprocess
from dataclasses import fields
import evdev

from .SteeringDeviceConfig import SteeringDeviceConfig, ButtonData, Buttons


class SteeringDevice:

    def __init__(self, config: SteeringDeviceConfig):
        self.__conf = config
        self.__initController(config.DeviceVendorID)

    def __setSteeringValues(self, event: evdev.InputEvent) -> Buttons:
        """
        Setting the values of the steering-device inside the Buttons object, which is defined in ControllerConfig.
        :param event: Event that has been triggered.
        :return: Buttons object containing the ids and values of the steering-device.
        """
        for field in fields(self.__conf.buttons):
            fieldContent = getattr(self.__conf.buttons, field.name)
            if not isinstance(fieldContent, ButtonData):
                continue
            if fieldContent.ID == event.code:
                fieldContent.value = event.value
        return self.__conf.buttons

    def __initController(self, vendorID: int) -> None:
        """
        Automatically detects and connects the controller with the vendor-ID specified in Configurations.conf! Only works on linux!
        :param vendorID: Device-id used for identification and automatic discovery of the controller.
        """
        path = self.__conf.ControllerPath
        directoryListing = subprocess.Popen(['ls', path], stdout=subprocess.PIPE).communicate()
        deviceList = (directoryListing[0]).decode().split('\n')
        """Checking if device meets the preset vendor-id. If so setting it as the controller."""
        for device in deviceList:
            device = f'{path}{device}'
            if 'event' not in device:
                continue
            # setting the device to a file of the input-directory
            device = evdev.InputDevice(device)
            # checking for the vendor-id of the device. If it matches the configured id in SteeringDeviceConfig.py
            # the device will be set as controller and the method returns (None). If no matching device found,
            # raising exception!
            if device.info.vendor == vendorID:
                self.__controller = device
                return
        raise TypeError('SteeringInput not found!')

    def readController(self, callbackMethod: callable) -> None:
        """
        Method for reading the controller in a loop.
        :param callbackMethod: Method that the controller-output will be delivered to.
        """
        self.__controller.grab()  # makes the controller only listen to this Code
        for event in self.__controller.read_loop():
            if event.type == 0:
                continue
            callbackMethod(self.__setSteeringValues(event))
