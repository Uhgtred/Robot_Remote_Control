#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Events import EventManager


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


if __name__ == '__main__':
    unittest.main()
