#!/usr/bin/env python3
# @author: Markus Kösters

import asyncio
import time

from Runners.runner import Runner


class AsyncTasks(Runner):

    def runTask(self, task: callable, *args) -> None:
        asyncio.run(self.__asyncTask(task))

    async def __runAsync(self, task: callable, *args):
        """
        Creating an asynchronous task, that can be awaited.
        :param task: Task that will be executed.
        :param args: Parameters that will be passed to that task.
        """
        asyncTask = asyncio.create_task(self.__asyncTask(task, *args))
        await asyncTask

    async def __asyncTask(self, task: callable, *args):
        """
        Method executing a task asynchronously.
        :param task: Task that will be executed.
        :param args: Parameters that will be passed to that task.
        """
        task(*args)

if __name__ == '__main__':
    def test1():
        asyncio.sleep(5)

    def test2():
        asyncio.sleep(2)

    def test():
        asyncio.sleep(4)

    obj = AsyncTasks()
    start = time.time()
    obj.runTask(test)
    obj.runTask(test1)
    obj.runTask(test2)
    print(time.time() - start)
