#!/usr/bin/env python3
# @author: Markus Kösters

from weakref import WeakSet

import ProjectLogging
from Events.EventInterface import EventInterface


class Event(EventInterface):
    """
    This class implements an event subscription and notification mechanism.

    The Event class allows external methods or functions to subscribe to it
    and receive updates (notifications) whenever an event occurs. The subscribers
    can be notified with data, and there is an optional verbose mode for detailed
    logging of the notification process.

    :ivar __logger: An instance of the logger used for logging event-related
        notifications and associated details.
    :type __logger: ProjectLogging.Logger.getLogger
    """

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Events', 'Events.log').getLogger

    def __init__(self) -> None:
        self.__subscribers: WeakSet = WeakSet()

    def subscribe(self, callbackMethod: callable) -> None:
        """
        Subscribing to Event, receiving any updates occurring.
        :param callbackMethod: Method that the event-update is going to be sent to.
        """
        self.__logger.info(f'Subscribing to Event with callback-method: {callbackMethod.__name__}!'
                           f'List of subscribers: {self.__subscribers}')
        self.__subscribers.add(callbackMethod)

    def notifySubscribers(self, data: any) -> None:
        """
        Notifies all subscribers by invoking their callback methods with the provided data.

        This method iterates through the list of subscriber callback methods and calls each
        one, passing the given data as an argument. Subscribers must have registered their
        callback functions beforehand to receive notifications.

        :param data: The information or payload to send to all subscribers. The data is
            forwarded to each subscriber's callback method.

        :return: This method does not return any value.
        """
        for callbackMethod in self.__subscribers:
            callbackMethod(data)

    def notifySubscriberVerbose(self, data: any) -> None:
        """
        Notifies all subscribers with the provided data and logs relevant information.

        This method logs the list of current subscribers and the provided
        data input before invoking the notification process. It ensures all
        subscribers are properly updated with the supplied data.

        :param data: The data to notify the subscribers with.
        :type data: any
        :return: None
        :rtype: None
        """
        self.__logger.info(f'Subscribers:\t{self.__subscribers}\nArgument:\t{data}')
        self.notifySubscribers(data)
