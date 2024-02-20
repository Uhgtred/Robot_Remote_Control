#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class Runner(ABC):

    @abstractmethod
    def runTask(self, task: callable, *args) -> None:
        """
        Abstract method for defining how tasks shall be executed.
        :param task: Method that will be executed.
        :param args: Arguments that will be passed to this method.
        """
        pass
