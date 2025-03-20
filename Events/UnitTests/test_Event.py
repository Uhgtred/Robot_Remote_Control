#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Events import EventManager, Event


class MyEvent(unittest.TestCase):
    var = None

    def myFunction(self, arg):
        if arg:
            self.var = arg


class test_Event(unittest.TestCase):
    event = EventManager().produceEvent('testEvent')
    myEvent = MyEvent()

    def test_subscribe(self):
        self.event.subscribe(self.myEvent.myFunction)
        self.assertTrue(self.myEvent.myFunction in self.event._Event__subscribers)

    def test_notifySubscribers(self):
        self.event.subscribe(self.myEvent.myFunction)
        self.event.notifySubscribers('Hello World!')
        self.assertEqual(self.myEvent.var, 'Hello World!')

    def test_event_instance_subscribers_independence(self):
        """
        Verifies that each Event instance maintains its own set of subscribers,
        ensuring no cross-subscriber notifications between different events.
        """
        # Create two separate Event instances
        event1 = Event()
        event2 = Event()

        # Define two separate subscriber functions
        subscriber1_data = []
        subscriber2_data = []

        def subscriber1(arg):
            subscriber1_data.append(arg)

        def subscriber2(arg):
            subscriber2_data.append(arg)

        # Subscribe functions to their respective events
        event1.subscribe(subscriber1)
        event2.subscribe(subscriber2)

        # Notify subscribers of each event
        event1.notifySubscribers("Event1 Message")
        event2.notifySubscribers("Event2 Message")

        # Assert that only the correct subscribers were notified
        self.assertEqual(subscriber1_data, ["Event1 Message"])
        self.assertEqual(subscriber2_data, ["Event2 Message"])

        # Ensure each event's subscriber list is independent
        self.assertNotIn(subscriber2, event1._Event__subscribers)
        self.assertNotIn(subscriber1, event2._Event__subscribers)


if __name__ == '__main__':
    unittest.main()
