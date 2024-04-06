import unittest
from unittest.mock import Mock, patch

import evdev

from SteeringInput import SteeringDevice
from SteeringInput.SteeringDeviceConfig import SteeringDeviceConfig, ButtonsInterface, ButtonsXBox


class TestSteeringDevice(unittest.TestCase):

    @patch('evdev.InputDevice')
    def setUp(self, mock_evdev):
        # Set up a SteeringDevice instance for testing
        config = SteeringDeviceConfig()
        self.device = SteeringDevice(config)
        # Mock evdev library methods
        self.mock_evdev = mock_evdev

    @patch('evdev.InputDevice')
    def test_init_controller(self, mock_InputDevice):
        mock_vendor = 1118
        mock_response = Mock()
        mock_response.info.vendor = mock_vendor
        mock_InputDevice.return_value = mock_response
        # Test successful initController
        self.device.initController(mock_vendor)
        self.assertIsNotNone(self.device._SteeringDevice__controller)
        # Test failed initController - will raise TypeError
        mock_response.info.vendor = 0
        with self.assertRaises(TypeError):
            self.device.initController(mock_vendor)

    def test_set_steering_values(self):
        # Mock event
        mock_event = Mock()
        mock_event.code = 1
        mock_event.value = 2
        # Test set_steering_values
        result = self.device._SteeringDevice__setSteeringValues(mock_event)
        self.assertIsInstance(result, ButtonsXBox)  # Check if the result is an instance of Buttons

    @patch('subprocess.Popen')
    def test_search_available_devices(self, mock_popen):
        mock_path = '/dev/input/'
        # Mock subprocess.Popen
        mock_popen.return_value.communicate.return_value = (b'event0\nevent1\n', b'')
        devices_list = self.device._SteeringDevice__searchAvailableDevices(mock_path)
        self.assertListEqual(devices_list, ['event0', 'event1'])  # Check if the list of devices is correct

    def test_check_vendor_id(self):
        mock_device = Mock()
        mock_vendor = 1234
        mock_device.info.vendor = mock_vendor
        # Test successful __checkVendorID
        self.device._SteeringDevice__checkVendorID(mock_device, mock_vendor)
        # Test failed __checkVendorID - will raise TypeError
        mock_device.info.vendor = 0
        with self.assertRaises(TypeError):
            self.device._SteeringDevice__checkVendorID(mock_device, mock_vendor)

    @patch('evdev.InputDevice.read_loop')
    def test_read_controller(self, mock_read_loop):
        mock_read_loop.return_value = []
        # Mock callback method
        mock_callback = Mock()
        # Test readController
        self.device.readController(mock_callback)
        mock_callback.assert_not_called()  # As the read_loop returns an empty list, the callback should never be called


if __name__ == '__main__':
    unittest.main()