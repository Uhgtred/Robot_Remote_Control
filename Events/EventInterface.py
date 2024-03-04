#!/usr/bin/env python3
# @author: Markus Kösters

from Events.EventManager import EventManager


class EventInterface:

    @staticmethod
    def subscribeToEvent(eventName: str, callbackMethod: callable) -> None:
        """
        Method for subscribing to an existing Event.
        :param eventName: Clear name of the event. Existing events can be received by calling getEventsList.
        :param callbackMethod: Method that is going to be used to call back when event-update occurs.
        """
        event = EventManager.produceEvent(name=eventName)
        event.subscribe(callbackMethod=callbackMethod)

    @staticmethod
    def postEventUpdate(eventName: str, data: any) -> None:
        """
        Method for notifying subscribers of an event.
        :param eventName: Clear name of the event. Existing events can be received by calling getEventsList.
        :param data: Data that will be shared to the subscribers.
        """
        event = EventManager.produceEvent(name=eventName)
        event.notifySubscribers(data=data)
