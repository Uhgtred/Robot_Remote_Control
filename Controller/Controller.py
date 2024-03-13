#!/usr/bin/env python3
# @author   Markus Kösters

import subprocess
# import libevdev
import evdev

from .ControllerConfig import ControllerConfig


class Controller:

    def __init__(self, config: ControllerConfig):
        self.__conf = config
        self.__initController(config.DeviceVendorID)

    def __defineButtonConfig(self, config: ControllerConfig) -> None:
        """Defining the values of the buttons. Button-IDs can be changed in the config-file"""
        """ORDER OF THE DICTIONARY DOES MATTER FOR RobotController.ino ON ROBOT!!!"""
        """TODO: Change this, so there is no dependance on the structure of the dictionary for the interpretation on the arduino!"""
        self.__buttonDict = {config.RTrigger: 0,
                             config.RBtn: 0,
                             config.LTrigger: 0,
                             config.LBtn: 0,
                             config.RXAxis: 0,
                             config.RYAxis: 0,
                             config.LXAxis: 0,
                             config.LYAxis: 0,
                             config.L3: 0,
                             config.R3: 0,
                             config.StartBtn: 0,
                             config.SelectBtn: 0,
                             config.ABtn: 0,
                             config.BBtn: 0,
                             config.XBtn: 0,
                             config.YBtn: 0,
                             config.XCross: 0,
                             config.YCross: 0
                             }

    def __initController(self, vendorID: int) -> None:
        """
        Automatically detects and connects the controller with the vendor-ID specified in Configurations.conf! Only works on linux!
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
            # checking for the vendor-id of the device. If it matches the configured id in ControllerConfig.py
            # the device will be set as controller and the method returns (None). If no matching device found,
            # raising exception!
            if device.info.vendor == vendorID:
                self.__controller = device
                return
        raise TypeError('Controller not found!')

    def readController(self, callbackMethod: callable) -> None:
        """
        Method for reading the controller in a loop.
        """
        # self.__controller.grab()  # makes the controller only listen to this Code
        self.__defineButtonConfig(self.__conf)
        for event in self.__controller.read_loop():
            if event.type == 0:
                continue
            self.__processControllerValues(event, callbackMethod)

    def __processControllerValues(self, event: evdev.events, callbackMethod: callable) -> None:
        """
        Method for analyzing the events on the controller and delivering the right data to the transmitter-method.
        :param event: Controller-Event that will be analyzed.
        :param callbackMethod: Method that will be used to send the current event-data to.
        """
        if event.code == self.__conf.LBtn or event.code == self.__conf.RBtn:
            self.__buttonDict[event.code] = (0 if not event.value else 1)
        else:
            self.__buttonDict[event.code] = event.value
        self.__transmitControllerValues(callbackMethod)

    def __transmitControllerValues(self, callbackMethod: callable) -> None:
        """
        Method for retrieving controller-values and returning them in a csv-style.
        :return: string with controller-values in csv-format.
        """
        tempList = []
        for key in self.__buttonDict:
            keyValue = self.__buttonDict.get(key)
            # Values can be a list if controller-element has axes.
            if type(keyValue) is list:
                # making sure the value is not greater than 255 for controller-elements with axes.
                tempList.append(round(keyValue[0] / 128.5) if keyValue[0] != 0 else 0)
                tempList.append(round(keyValue[1] / 128.5) if keyValue[1] != 0 else 0)
            else:
                tempList.append(keyValue)
        contValues = ','.join(str(element) for element in tempList)
        print(contValues)
        # returning controller-output
        callbackMethod(contValues)
