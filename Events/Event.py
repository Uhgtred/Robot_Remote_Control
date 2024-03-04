#!/usr/bin/env python3
# @author: Markus Kösters


class Event:
    """
    Class that represents an event which can be subscribed to and posted to.
    """

    __subscribers: set = set()

    def subscribe(self, callbackMethod: callable) -> None:
        """
        Subscribing to Event, receiving any updates occurring.
        :param callbackMethod: Method that the event-update is going to be sent to.
        """
        self.__subscribers.add(callbackMethod)

    def notifySubscribers(self, data: any) -> None:
        """
        Sending an Event-update to all subscribers.
        :param data: Message-data that shall be sent to subscribers.
        """
        for callbackMethod in self.__subscribers:
            callbackMethod(data)
