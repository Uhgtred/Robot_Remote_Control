#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from SteeringInput import SteeringDevice
from SteeringInput.SteeringDeviceFactory import SteeringDeviceFactory


class test_SteeringDeviceFactory(unittest.TestCase):

    def setUp(self):
        self.factory = SteeringDeviceFactory()

    def test_produceController(self):
        controller = self.factory.produceControllerWithoutInitOfController()
        self.assertIsInstance(controller, SteeringDevice)


if __name__ == '__main__':
    unittest.main()
