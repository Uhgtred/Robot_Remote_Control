#!/usr/bin/env python3
# @author: Markus Kösters

import asyncio
import time

from Runners.runner import Runner


class AsyncRunner:
    """
    Class for running async tasks.
    """

    __tasks: list = []
    __asyncTasks: list = []
    __running: bool = False

    def addTask(self, task, *args) -> None:
        """
        Method that adds a task to the list of tasks.
        :param task:    Method or Function that will be executed by the runner.
        :param args:    Arguments passed to the Method that will be run.
                        Needs at least a callback-method if there is any return expected.
        """
        task.args = [*args]
        self.__tasks.append(task)

    def runTasks(self) -> None:
        """
        Method that starts processing all tasks waiting for execution.
        """
        if not self.__running:
            self.__running = True
            asyncio.run(self.__runAsync())

    def stopTasks(self) -> None:
        """
        Method that stops the execution of this module.
        """
        if self.__running:
            self.__running = False

    async def __runAsync(self):
        """
        Method that runs all the waiting tasks in a loop until running-flag is set to false and there are no more open tasks to complete.
        """
        while self.__running:
            # converting tasks into async tasks and throwing them into a list.
            for task in self.__tasks:
                asyncTask = asyncio.create_task(self.__asyncTask(task, *task.args))
                self.__asyncTasks.append(asyncTask)
                self.__tasks.remove(task)
            # running and awaiting async tasks.
            for asyncTask in self.__asyncTasks:
                await asyncTask
                self.__asyncTasks.remove(asyncTask)

    async def __asyncTask(self, task: callable, *args):
        """
        Method executing a task asynchronously.
        :param task: Task that will be executed.
        :param args: Parameters that will be passed to that task.
        """
        response = await asyncio.to_thread(task, *args)
        return response
