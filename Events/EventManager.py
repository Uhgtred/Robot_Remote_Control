#!/usr/bin/env python3
# @author      Markus Kösters

from .Event import Event


class EventManager:
    """
    Factory-class for EventUser.
    """

    __events: dict = {}

    @classmethod
    def produceEvent(cls, name: str) -> Event:
        """
        Method producing a new event.
        :return:    An instance of an Event, that can be used to create an update
                    for the subscribers and for subscribing to this event.
        """
        # Only adds the key to the dictionary if it does not already exist!
        cls.__events.setdefault(name, Event())
        return cls.__events.get(name)

    @property
    def getEventsList(self) -> list[str]:
        """
        Getter Method for Events available.
        :return: List of available Events.
        """
        return list(self.__events.keys())
