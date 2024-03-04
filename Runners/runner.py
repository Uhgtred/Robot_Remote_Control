#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class Runner(ABC):

    @abstractmethod
    def addTask(self, task, *args) -> None:
        """
        Method that adds a task to the list of tasks.
        :param task:    Method or Function that will be executed by the runner.
        :param args:    Arguments passed to the Method that will be run.
                        Needs at least a callback-method if there is any return expected.
        """

    @abstractmethod
    def runTasks(self) -> None:
        """
        Method that starts processing all tasks waiting for execution.
        """

    @abstractmethod
    def stopTasks(self) -> None:
        """
        Method that stops the execution of this module.
        """
