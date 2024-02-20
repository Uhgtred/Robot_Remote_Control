#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time

from Configurations.ConfigReader import ConfigReader
from Controller.Controller import Controller
from Network.SocketController import SocketController
# from Remote.MainGUI import MainGUI


class Main:

    def __init__(self):
        """Starting the Remote-Program and configuring everything"""
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.socketController = SocketController()
        self.__cont = Controller()
        # self.mainGUI = MainGUI()
        self.__threads()

    def __readController(self):
        self.socketController.connectToServer('controller')
        while True:
            self.socketController.sendMessage(self.__cont.getControllerValues, 'controller')
            time.sleep(self.__delay)

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        __controllerReadThread = threading.Thread(target=self.__cont.readController, name='ControllerReadThread', daemon=True)
        __controllerReadThread.start()

        __controllerThread = threading.Thread(target=self.__readController, name='ControllerThread', daemon=True)
        __controllerThread.start()

        # __cameraStreamThread = threading.Thread(target=self.mainGUI.startGUI, name='CameraStreamThread', daemon=True)
        # __cameraStreamThread.start()

        __controllerThread.join()
        __controllerReadThread.join()
        # __cameraStreamThread.join()

    def exit_handler(self):
        """Put things that need to be done before program-exit"""
        pass


main = Main()
