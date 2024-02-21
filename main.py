#!/usr/bin/env python3
# @author   Markus Kösters

from BusTransactions.BusFactory import BusFactory
from Controller import ControllerFactory
from Runners import asyncRunner


# from Remote.MainGUI import MainGUI


class Main:

    def __init__(self):
        """Starting the Remote-Program and configuring everything"""
        # self.mainGUI = MainGUI()
        self.__asyncRunner = asyncRunner.AsyncRunner()

    def __readController(self) -> None:
        """
        Method for reading the controller and sending its messages to the robot.
        """
        udpBus = BusFactory.produceUDP_Transceiver()
        controller = ControllerFactory.produceController()
        self.__asyncRunner.addTask(controller.readController, udpBus.writeSingleMessage)

    def exit_handler(self):
        """Put things that need to be done before program-exit"""
        pass


if __name__ == '__main__':
    main = Main()
