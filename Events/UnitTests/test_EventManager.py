#!/usr/bin/env python3
# @author Markus Kösters

import unittest

from Events import EventManager


class test_EventManager(unittest.TestCase):
    eventManager = EventManager()

    def test_ProduceEvent(self):
        self.eventManager.produceConcreteEvent('testEvent')
        self.assertIn('testEvent', self.eventManager.getEventsList)


if __name__ == '__main__':
    unittest.main()
