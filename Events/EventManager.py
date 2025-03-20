#!/usr/bin/env python3
# @author      Markus Kösters

import logging

from .Event import Event


class EventManager:
    """
    Factory-class for EventUser.
    """

    __events: dict = {}
    __logger: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def produceEvent(cls, name: str) -> Event:
        """
        Method producing a new event.
        :return:    An instance of an Event, that can be used to create an update
                    for the subscribers and for subscribing to this event.
        """
        # Only adds the key to the dictionary if it does not already exist!
        cls.__events.setdefault(name, Event())
        EventManager.__logger.debug(f'Event {name} created.')
        return cls.__events.get(name)

    @property
    def getEventsList(self) -> list[str]:
        """
        Getter Method for Events available.
        :return: List of available Events.
        """
        return list(self.__events.keys())

    def subscriberEvent(self, eventName: str, callbackMethod: callable) -> None:
        """
        Subscribes a callback method to a specific event if the provided callback
        is callable. Associates the callback with the given event name if such an
        event exists in the internal events registry.

        :param eventName: The name of the event to which the callback should be
            subscribed.
        :type eventName: str
        :param callbackMethod: The callable method or function to be subscribed
            to the specified event. Must be a callable object.
        :type callbackMethod: callable
        :return: This method does not return any value.
        :rtype: None
        """
        if not callable(callbackMethod):
            return
        self.__events.get(eventName).subscribe(callbackMethod)

