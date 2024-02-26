#!/usr/bin/env python3
# @author   Markus Kösters

import subprocess
from evdev import InputDevice

from .ControllerConfig import ControllerConfig


class Controller:

    __controller = None
    __buttonDict = None

    def __init__(self, config: ControllerConfig):
        self.__conf = config
        self.__deviceVendor = config.DeviceVendorID
        self.__defineButtonConfig(config)
        self.__initController()

    def __defineButtonConfig(self, config: ControllerConfig) -> None:
        """Defining the values of the buttons. Button-IDs can be changed in the config-file"""
        """ORDER OF THE DICTIONARY DOES MATTER FOR RobotController.ino ON ROBOT!!!"""
        """TODO: Change this, so there is no dependance on the structure of the dictionary for the interpretation on the arduino!"""
        self.__buttonDict = {config.RTrigger: 0,
                             config.RBtn: 0,
                             config.LTrigger: 0,
                             config.LBtn: 0,
                             config.RXAxis: [0, 0],
                             config.RYAxis: [0, 0],
                             config.LXAxis: [0, 0],
                             config.LYAxis: [0, 0],
                             config.L3: 0,
                             config.R3: 0,
                             config.StartBtn: 0,
                             config.SelectBtn: 0,
                             config.ABtn: 0,
                             config.BBtn: 0,
                             config.XBtn: 0,
                             config.YBtn: 0,
                             config.XCross: [0, 0],
                             config.YCross: [0, 0]
                             }

    def __initController(self) -> None:
        """
        Automatically detects and connects the controller with the vendor-ID specified in Configurations.conf! Only works on linux!
        """
        path = self.__conf.ControllerPath
        directoryListing = subprocess.Popen(['ls', path], stdout=subprocess.PIPE).communicate()
        # directoryListing = directoryListing.communicate()
        deviceList = (directoryListing[0]).decode()
        deviceList = deviceList.split('\n')
        """Checking if device meets the preset vendor-id. If so setting it as the controller."""
        for device in deviceList:
            device = f'{path}{device}'
            if 'event' in device:
                if InputDevice(device).info.vendor == self.__deviceVendor:
                    self.__controller = InputDevice(device)

    def readController(self, callbackMethod: callable) -> None:
        """
        Method for reading the controller in a loop.
        """
        self.__controller.grab()  # makes the controller only listen to this Code
        for event in self.__controller.read_loop():
            self.__processControllerValues(event, callbackMethod)

    def __processControllerValues(self, event: InputDevice.Event, callbackMethod: callable) -> None:
        """
        Method for analyzing the events on the controller and delivering the right data to the transmitter-method.
        :param event: Controller-Event that will be analyzed.
        :param callbackMethod: Method that will be used to send the current event-data to.
        """
        if event.code == self.__conf.LBtn or event.code == self.__conf.RBtn:
            self.__buttonDict[event.code] = (0 if not event.value else 1)
        else:
            if event.value < 0:
                self.__buttonDict[event.code][1] = abs(event.value)
            if type(self.__buttonDict.get(event.code)) is list:
                self.__buttonDict[event.code][0] = event.value
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
        # returning controller-output
        callbackMethod(contValues)
