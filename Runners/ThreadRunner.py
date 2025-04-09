#!/usr/bin/env python3
# @author: Markus Kösters
import atexit
import threading

from Runners.AbstractRunner import Runner


class ThreadRunner(Runner):
    """
    Method for organizing threads and keeping track of opened tracks.
    """

    def __init__(self):
        self.__threads: list = []
        self.__running: bool = False
        # Todo: kill all threads that are still running
        # atexit.register()

    def addTask(self, task, *args, **kwargs) -> None:
        """
        Method for adding a task to the task-list.
        :param task: Method that shall be executed in a separate thread.
        :param args: Arguments, that shall be passed to the thread.
        """
        thread = threading.Thread(target=task, args=args, name=f'{str(task).split(" ")[1]}_thread')
        self.__threads.append(thread)

    def runTasks(self) -> None:
        """
        Method for running all .
        """
        if self.__running:
            return
        self.__running = True
        while self.__running and len(self.__threads) > 0:
            self.__threads.pop().start()
        self.__running = False

    def stopTasks(self) -> None:
        """
        Method for stopping the thread-execution.
        """
        self.__running = False
