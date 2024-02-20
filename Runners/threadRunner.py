#!/usr/bin/env python3
# @author: Markus Kösters

import threading

from Runners.runner import Runner


class Threads(Runner):
    """
    Method for organizing threads and keeping track of opened tracks.
    """

    __threads: dict = {}

    def runTask(self, task: callable, *args) -> None:
        """
        Method for running a passed method in a new thread.
        :param task: Method that shall be executed in a separate thread.
        :param args: Arguments, that shall be passed to the thread.
        """
        args = list(*args)
        threadName = f'{str(task).split(" ")[1]}_thread'
        thread = threading.Thread(target=task, args=args, name=threadName)
        self.__threads[threadName] = thread
        thread.start()
