#!/usr/bin/env python3
# @author      Markus Kösters

import logging

from .AbstractEvent import AbstractEvent


class EventManager:
    """
    Manages events, allowing event production, subscription, and retrieval.

    The EventManager class provides functionality to manage an event-driven system.
    It allows creating new events, subscribing methods or functions to those events,
    and retrieving a list of all available events. Events can be used as a mechanism
    to notify subscribers of state changes or actions within the system.

    :ivar __events: Dictionary holding event names as keys and their corresponding
        Event instances as values.
    :type __events: dict
    """

    __events: dict = {}
    __logger: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def produceConcreteEvent(cls, name: str) -> AbstractEvent:
        """
        Method producing a new event.
        :return:    An instance of an Event, that can be used to create an update
                    for the subscribers and for subscribing to this event.
        """
        # Only adds the key to the dictionary if it does not already exist!
        # If the key already exists in the dictionary, its value will be returned.
        return cls.__events.setdefault(name, AbstractEvent())

    @property
    def getEventsList(self) -> list[str]:
        """
        Provides a property to retrieve the list of event names from the internal events dictionary.

        :return: A list of strings containing the names of the events.
        :rtype: list[str]
        """
        return list(self.__events.keys())

    def subscribeToEvent(self, eventName: str, callbackMethod: callable) -> None:
        """
        Method for subscribing to a specific event.
        :param callbackMethod: Method that will be used for the callback (event update).
        :param eventName: Name of the event.
        """
        if not callable(callbackMethod):
            raise TypeError(f'Callbackmethod: {callbackMethod} is not callable!')
        self.__events.get(eventName).subscribe(callbackMethod)

