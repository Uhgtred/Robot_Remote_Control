#!/usr/bin/env python3
import atexit
import concurrent.futures
import inspect
import sys
from concurrent.futures import ThreadPoolExecutor, Future
from threading import Event
from typing import Callable, Dict

import ProjectLogging
from .AbstractRunner import AbstractRunner


class ThreadRunner(AbstractRunner):
    """
    Represents a threaded task runner for managing and executing tasks concurrently.

    The ThreadRunner is designed to facilitate the execution of multiple tasks with
    thread pooling. It enables task submission, tracking, stopping, and resource
    cleanup, leveraging a thread pool executor for concurrency.

    :ivar max_workers: Maximum number of workers for thread pool executor.
    :type max_workers: int
    """

    __logger = ProjectLogging.Logger(__name__, f'{__name__}.log').getLogger

    def __init__(self, max_workers: int = None) -> None:
        """
        Initializes a custom threaded Executor with a specified maximum number of workers.

        This class implements a thread pool executor and maintains a registry of futures
        to manage asynchronous tasks. The number of worker threads can be customized,
        and the tasks submitted will run concurrently within the pool.

        :param max_workers: The maximum number of threads that can be used to execute tasks.
            If None, the default value is used, which is derived from the system configuration.
        :type max_workers: int, optional
        """
        super().__init__()
        self.__executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=max_workers)
        self.__futures: Dict[str, Future] = {}
        self.__stop_event: Event = Event()
        # Don't register atexit handler in test environments to prevent infinite loops
        # Tests should call cleanUp explicitly in tearDown methods
        if 'unittest' not in sys.modules:
            atexit.register(self.cleanUp)

    def addTask(self, task: Callable, *args, **kwargs) -> str:
        """
        Adds a task to the executor for execution.

        This method allows submission of a callable task, along with its positional
        and keyword arguments, to be executed asynchronously. The submitted task
        is associated with a unique identifier (task ID), which can be used for
        tracking or management purposes after the submission.

        :param task: Callable object representing the task to execute.
        :param args: Positional arguments to be passed to the task.
        :param kwargs: Keyword arguments to be passed to the task.
        :return: A unique string identifier (task ID) for the submitted task.
        :rtype: str
        """
        if not self.__checkTaskSignature(task, 1):
            raise ValueError(f"Task {task.__name__} does not have enough arguments in its signature.")
        task_id: str = str(id(task))
        future: concurrent.futures.Future = self.__executor.submit(task, *args, **kwargs)
        self.__futures[task_id]: concurrent.futures.Future = future
        return task_id

    def __checkTaskSignature(self, task: callable, minNumberofArgumentsInSignature: int) -> bool:
        """
        Checks whether the given task function has at least the specified minimum number
        of arguments in its signature. The function's signature is inspected to count
        the number of parameters and determine compliance with the given threshold.

        :param task: The callable task whose signature needs to be checked.
        :param minNumberofArgumentsInSignature: The minimum number of arguments
            required in the signature of the given callable.
        :return: A boolean value indicating whether the task has at least the
            required number of arguments in its signature.
        :rtype: bool
        """
        signature: inspect.Signature = inspect.signature(task)
        return True if len(signature.parameters) >= minNumberofArgumentsInSignature else False

    def stopTasks(self) -> None:
        """
        Stops and cancels all ongoing tasks managed by the instance.

        This method iterates through all current futures, cancels them, shuts down the
        executor service without waiting for tasks to complete, and clears the
        internal future tracking collection. Use this method when you need to
        terminate all asynchronous tasks immediately.

        :return: None
        """
        for future in self.__futures.values():
            future.cancel()
        self.__executor.shutdown(wait=False, cancel_futures=True)
        self.__futures.clear()

    def cleanUp(self) -> None:
        """
        Stops all running tasks and performs cleanup operations.

        This method ensures that any background tasks or ongoing processes associated with
        the object are stopped gracefully. It is intended to clean up resources and prepare
        the system for a safe shutdown or reinitialization.

        :return: None
        """
        self.stopTasks()
