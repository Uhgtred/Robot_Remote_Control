import unittest
from unittest.mock import Mock, patch

import evdev
from evdev import InputDevice

from SteeringInput import SteeringDevice
from SteeringInput.SteeringDeviceConfig import SteeringDeviceConfig, ButtonsInterface, ButtonsXBox


class TestSteeringDevice(unittest.TestCase):

    def setUp(self):
        # Set up a SteeringDevice instance for testing
        config = SteeringDeviceConfig()
        # Mock evdev library methods
        self.steeringDeviceClassObject = SteeringDevice(config)

    @patch('evdev.InputDevice')
    def test_init_controller(self, mock_InputDevice):
        mock_vendor = 1118
        mock_response = Mock()
        mock_response.info.vendor = mock_vendor
        mock_InputDevice.return_value = mock_response
        self.steeringDeviceClassObject.initController(mock_vendor)
        self.assertIsNotNone(self.steeringDeviceClassObject._SteeringDevice__controller)
        # Test failed initController - will raise TypeError
        mock_response.info.vendor = 0
        with self.assertRaises(TypeError):
            self.steeringDeviceClassObject.initController(mock_vendor)

    def test_set_steering_values(self):
        # Mock event
        mock_event = Mock()
        mock_event.code = 1
        mock_event.value = 2
        # Test set_steering_values
        result = self.steeringDeviceClassObject._SteeringDevice__setSteeringValues(mock_event)
        self.assertIsInstance(result, ButtonsXBox)  # Check if the result is an instance of Buttons

    @patch('subprocess.Popen')
    def test_search_available_devices(self, mock_popen):
        mock_path = '/dev/input/'
        # Mock subprocess.Popen
        mock_popen.return_value.communicate.return_value = (b'event0\nevent1\n', b'')
        devices_list = self.steeringDeviceClassObject._SteeringDevice__searchAvailableDevices(mock_path)
        self.assertListEqual(devices_list, ['event0', 'event1'])  # Check if the list of devices is correct

    def test_check_vendor_id(self):
        mock_device = Mock()
        mock_vendor = 1234
        mock_device.info.vendor = mock_vendor
        # Test successful __checkVendorID
        self.steeringDeviceClassObject._SteeringDevice__checkVendorID(mock_device, mock_vendor)
        # Test failed __checkVendorID - will raise TypeError
        mock_device.info.vendor = 0
        with self.assertRaises(TypeError):
            self.steeringDeviceClassObject._SteeringDevice__checkVendorID(mock_device, mock_vendor)

    @patch('evdev.InputDevice')
    def test_read_controller(self, mock_inputDevice):
        mock_event_response = Mock()
        mock_event_response.event.type: int = 1
        mock_event = mock_event_response
        mock_vendor = 1118
        mock_inputDevice_response = Mock()
        mock_inputDevice_response.info.vendor = mock_vendor
        mock_inputDevice_response.read_loop.return_value = [mock_event]
        mock_inputDevice.return_value = mock_inputDevice_response
        self.steeringDeviceClassObject.initController(mock_vendor)
        # Test readController
        self.steeringDeviceClassObject.readController(self.callbackHelperMethod)

    def callbackHelperMethod(self, event):
        self.assertIsInstance(event, ButtonsXBox)

if __name__ == '__main__':
    unittest.main()
