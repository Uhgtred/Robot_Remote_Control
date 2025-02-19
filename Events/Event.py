#!/usr/bin/env python3
# @author: Markus Kösters

import ProjectLogging


class Event:
    """
    Class that represents an event which can be subscribed to and posted to.
    """

    __subscribers: set = set()
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Events', 'Events.log').getLogger

    def subscribe(self, callbackMethod: callable) -> None:
        """
        Subscribing to Event, receiving any updates occurring.
        :param callbackMethod: Method that the event-update is going to be sent to.
        """
        self.__subscribers.add(callbackMethod)

    def notifySubscribers(self, data: any, verbose: bool = False) -> None:
        """
        Notifies all subscribers with the given data, allowing for an optional verbose mode
        that logs detailed information about the notification process.

        This method iterates through all registered subscriber callback methods
        and invokes them with the provided data. If `verbose` is enabled, the notification
        process logs the callback method name and the data being sent.

        :param data: The data to notify the subscribers with.
        :type data: any
        :param verbose: Indicates whether detailed logs about the notifications
            should be generated.
        :type verbose: bool
        :return: This method does not return anything.
        """
        for callbackMethod in self.__subscribers:
            if verbose:
                self.__logger.info(f'Event:\n\tCallback-method: {callbackMethod.__name__}\n\tArgument: {data}')
            callbackMethod(data)
