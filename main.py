#!/usr/bin/env python3
# @author   Markus Kösters

from BusTransactions.BusFactory import BusFactory
from Controller import ControllerFactory
from Runners import asyncRunner, threadRunner


# from Remote.MainGUI import MainGUI


class Main:

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
        udpBus = BusFactory.produceUDP_Transceiver(host=False, port=2001)
        controller = ControllerFactory.produceController()
        self.__asyncRunner.addTask(controller.readController, udpBus.writeSingleMessage)

    def __recvVideo


if __name__ == '__main__':
    main = Main()
