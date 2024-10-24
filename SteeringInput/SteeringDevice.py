#!/usr/bin/env python3
# @author   Markus Kösters

import subprocess
from dataclasses import fields
import evdev

from .SteeringDeviceConfig import SteeringDeviceConfig, ButtonData, ButtonsInterface


class SteeringDevice:

    def __init__(self, config: SteeringDeviceConfig):
        self.__conf = config
        self.__controller = None
        self.initController(config.DeviceVendorID)

    def __setSteeringValues(self, event: evdev.InputEvent) -> ButtonsInterface:
        """
        Setting the values of the steering-device inside the ButtonsInterface object, which is defined in ControllerConfig.
        :param event: Event that has been triggered.
        :return: ButtonsInterface object containing the ids and values of the steering-device.
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
        Automatically detects and connects the controller with the vendor-ID specified in Configurations.conf! Only works on linux!
        :param vendor: Vendor-ID of the controller.
        """
        if not vendor:
            vendor = self.__conf.DeviceVendorID
        path = self.__conf.ControllerPath
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
        Method for checking for the vendor-id of the device. If it matches the configured id in SteeringDeviceConfig.py
        the device will be set as controller, and the method returns (None). If no matching device found, raising exception!
        :param device: Device that the id is being checked against.
        :return: True if the vendor matches else False.
        """
        if device.info.vendor == vendor:
            self.__controller = device
            return True
        return False

    def __searchAvailableDevices(self, path: str) -> list:
        """
        Method for detecting any connected hardware.
        :param path: Path to where the devices are located.
        :return: List of connected hardware.
        """
        directoryListing = subprocess.Popen(['ls', path], stdout=subprocess.PIPE).communicate()
        return (directoryListing[0]).decode().strip().split('\n')

    def readController(self, callbackMethod: callable) -> None:
        """
        Method for reading the controller in a loop.
        :param callbackMethod: Method that the controller-output will be delivered to.
        """
        if not self.__controller:
            raise BaseException('No controller has been initialized!')
        self.__controller.grab()  # makes the controller only listen to this Code
        for event in self.__controller.read_loop():
            if event.type == 0:
                continue
            callbackMethod(self.__setSteeringValues(event))
