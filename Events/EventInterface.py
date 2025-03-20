#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod

from Events import Event


class EventInterface(ABC):

    @classmethod
    @abstractmethod
    def produceEvent(cls, name: str) -> Event:
        """
        Method producing a new event.
        :return:    An instance of an Event, that can be used to create an update
                    for the subscribers and for subscribing to this event.
        """

    @property
    @abstractmethod
    def getEventsList(self) -> list[str]:
        """
        Getter Method for Events available.
        :return: List of available Events.
        """