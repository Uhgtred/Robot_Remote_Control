#!/usr/bin/env python3
# @author: Markus Kösters

import unittest
from unittest.mock import patch, MagicMock

from SteeringInput import SteeringDevice
from SteeringInput.SteeringDeviceFactory import SteeringDeviceFactory


class test_SteeringDeviceFactory(unittest.TestCase):

    def setUp(self):
        self.factory = SteeringDeviceFactory()

    def test_produceControllerWithoutInitOfController(self):
        """Test the produceControllerWithoutInitOfController method."""
        controller = self.factory.produceControllerWithoutInitOfController()
        self.assertIsInstance(controller, SteeringDevice)

    @patch('SteeringInput.SteeringDevice.SteeringDevice.initController')
    def test_produceController(self, mock_init_controller):
        """Test the produceController method."""
        # Mock the initController method to avoid hardware access
        mock_init_controller.return_value = None

        # Call the method under test
        controller = self.factory.produceController()

        # Verify that the controller is a SteeringDevice
        self.assertIsInstance(controller, SteeringDevice)

        # Verify that initController was called
        mock_init_controller.assert_called_once()


if __name__ == '__main__':
    unittest.main()
