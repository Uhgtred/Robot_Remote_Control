#!/usr/bin/env python3
# @author: Markus Kösters

import asyncio
import time

from Runners.runner import Runner


class AsyncRunner:
    """
    Class for running async tasks. Can add multiple tasks before running the task-list.
    """

    __tasks: dict = {}
    __asyncTasks: list = []
    __running: bool = False

    def addTask(self, task, *args) -> None:
        """
        Method that adds a task to the list of tasks.
        :param task:    Method or Function that will be executed by the runner.
        :param args:    Arguments passed to the Method that will be run.
                        Needs at least a callback-method if there is any return expected.
        """
        # Adding the arguments of a task as an attribute to this task.
        # task.args = [*args]
        self.__tasks[task] = args
        # self.__asyncTasks.append(asyncio.create_task(self.__asyncTask(task, *task.args)))

    def runTasks(self) -> None:
        """
        Method that starts processing all tasks waiting for execution.
        """
        if self.__running:
            return
        self.__running = True
        asyncio.run(self.__runAsync())

    def stopTasks(self) -> None:
        """
        Method that stops the execution of this module.
        """
        self.__running = False

    async def __runAsync(self):
        """
        Method that runs all the waiting tasks in a loop until running-flag is set to false and there are no more open tasks to complete.
        """
        while self.__running and len(self.__tasks) > 0:
            # converting tasks into async tasks and throwing them into a list.
            task, args = self.__tasks.popitem()
            self.__asyncTasks.append(asyncio.create_task(self.__asyncTask(task, *args)))
        # running and awaiting async tasks.
        while len(self.__asyncTasks):
            await self.__asyncTasks.pop(0)
        self.__running = False

    async def __asyncTask(self, task: callable, *args):
        """
        Method executing a task asynchronously.
        :param task: Task that will be executed.
        :param args: Parameters that will be passed to that task.
        """
        response = await asyncio.to_thread(task, *args)
        return response
