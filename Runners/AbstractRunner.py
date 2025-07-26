#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class AbstractRunner(ABC):

    @abstractmethod
    def addTask(self, task, *args, **kwargs) -> None:
        """
        Adds a task to the task manager with optional arguments.

        This method is an abstract method designed to be implemented in a subclass.
        It serves as a framework for specifying the functionality of adding a task in
        the task management system. The specific implementation will depend on the
        subclass and could include various logic to handle, process, or prioritize
        tasks using the provided parameters.

        :param task: A task object or identifier that needs to be added to the task
            manager.
        :param args: Additional positional arguments that provide supplementary
            information or modify the behavior when adding the task.
        :param kwargs: Additional keyword arguments that provide more specific
            configuration or instructions for adding the task.
        :return: None

        """

    @abstractmethod
    def stopTasks(self) -> None:
        """
        This method serves as an abstract method that must be implemented by any subclass. The purpose of the method
        is to encapsulate the logic for stopping or terminating tasks. The exact implementation details will depend
        on the specific subclass and the nature of the tasks being stopped.

        This method is critical for defining behavior in classes that need explicit handling of stopping operations,
        ensuring that subclasses conform to the expected interface contract.

        :raises NotImplementedError: If the method is not implemented in a subclass.
        :rtype: None
        """
