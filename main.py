#!/usr/bin/env python3
# @author   Markus Kösters
from BusTransactions import Bus
from BusTransactions.BusFactory import BusFactory
from SteeringInput import SteeringDeviceFactory
from GUI.GUI_Contoller import GUI_Controller
from Runners import asyncRunner, threadRunner


# from Remote.MainGUI import MainGUI


class Main:

    __ports: dict = {'controllerPort': 2001, 'APIPort': 3000, 'videoPort': 2002}

    def __init__(self):
        """Starting the Remote-Program and configuring everything"""
        # self.mainGUI = MainGUI()
        self.__asyncRunner = asyncRunner.AsyncRunner()
        self.__threadRunner = threadRunner.ThreadRunner()
        self.__setup()
        self.__asyncRunner.runTasks()
        self.__threadRunner.runTasks()

    def __setup(self) -> None:
        """
        Method for setting up the program.
        """
        # Add any setup code here
        self.__readController()

    def __readController(self) -> None:
        """
        Method for reading the controller and sending its messages to the robot.
        """
        udpBus = BusFactory.produceUDP_Transceiver(host=False, port=self.__ports.get('controllerPort'))
        controller = SteeringDeviceFactory.produceController()
        self.__asyncRunner.addTask(controller.readController, udpBus.writeSingleMessage)

    def __recvVideo(self) -> None:
        """
        Method for receiving Video from the robot.
        """
        udpBus: Bus = BusFactory.produceUDP_Transceiver(host=False, port=self.__ports.get('videoPort'))
        videoController: GUI_Controller = GUI_Controller()
        self.__threadRunner.addTask(udpBus.readBusUntilStopFlag, videoController.updateRootView)


if __name__ == '__main__':
    main = Main()
