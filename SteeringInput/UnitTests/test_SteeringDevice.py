import unittest
from unittest.mock import MagicMock, patch
from evdev import InputDevice, InputEvent

from SteeringInput import SteeringDevice
from SteeringInput.ButtonsInterface import ButtonsInterface
from SteeringInput.SteeringDeviceConfig import SteeringDeviceConfig


# Import the SteeringDevice and related classes


class TestSteeringDevice(unittest.TestCase):

    @patch('evdev.InputDevice')
    @patch('subprocess.Popen')
    def test_initController(self, mock_popen, mock_input_device):
        # Create a mock SteeringDeviceConfig
        mock_config = MagicMock(spec=SteeringDeviceConfig)
        mock_config.DeviceVendorID = 1234
        mock_config.ControllerPath = "/dev/input/"

        # Mock the Popen call to simulate the directory listing for devices
        mock_popen.return_value.communicate.return_value = (b'event0\nevent1\n', b'')

        # Create the SteeringDevice instance with the mock config
        device = SteeringDevice(mock_config)

        # Mock the InputDevice constructor to simulate a successful device connection
        mock_device = MagicMock(spec=InputDevice)
        mock_device.info.vendor = 1234  # Simulate a matching vendor ID
        mock_input_device.return_value = mock_device

        # Initialize the controller (this should not raise any exceptions)
        device.initController(1234)

        # Assert that the controller was set correctly
        self.assertEqual(device._SteeringDevice__controller, mock_device)

    @patch('evdev.InputDevice')
    @patch('subprocess.Popen')
    def test_initController_device_not_found(self, mock_popen, mock_input_device):
        # Create a mock SteeringDeviceConfig
        mock_config = MagicMock(spec=SteeringDeviceConfig)
        mock_config.DeviceVendorID = 1234
        mock_config.ControllerPath = "/dev/input/"

        # Mock the Popen call to simulate the directory listing for devices
        mock_popen.return_value.communicate.return_value = (b'event0\n', b'')

        # Create the SteeringDevice instance with the mock config
        device = SteeringDevice(mock_config)

        # Mock the InputDevice constructor to simulate no matching device
        mock_device = MagicMock(spec=InputDevice)
        mock_device.info.vendor = 5678  # Simulate a different vendor ID
        mock_input_device.return_value = mock_device

        # Try to initialize the controller with the correct vendor (should raise TypeError)
        with self.assertRaises(TypeError):
            device.initController(1234)

    @patch('evdev.InputDevice')
    @patch('subprocess.Popen')
    def test_readController(self, mock_popen, mock_input_device):
        # Create a mock SteeringDeviceConfig
        mock_config = MagicMock(spec=SteeringDeviceConfig)
        mock_config.DeviceVendorID = 1234
        mock_config.ControllerPath = "/dev/input/"
        mock_config.buttons = SteeringDeviceConfig.buttons

        # Mock the Popen call to simulate the directory listing for devices
        mock_popen.return_value.communicate.return_value = (b'event0\n', b'')

        # Create the SteeringDevice instance with the mock config
        device: SteeringDevice = SteeringDevice(mock_config)

        # Mock the InputDevice constructor
        mock_device: MagicMock = MagicMock(spec=InputDevice)
        mock_device.info.vendor = 1234  # Simulate a matching vendor ID
        mock_input_device.return_value = mock_device

        # Initialize the controller
        device.initController(1234)

        # Simulate an input event from the controller (button press)
        mock_event = MagicMock(spec=InputEvent)
        mock_event.type = 1  # EV_KEY type
        mock_event.code = 30  # Key code (for example, 'A' button)
        mock_event.value = 1  # Pressed

        # Mock the controller's read_loop method
        mock_device.read_loop.return_value = [mock_event]

        # Mock the callback function to capture the processed buttons
        mock_callback: MagicMock = MagicMock()

        # Run the readController method and ensure the callback is called
        device.readController(mock_callback)

        # Assert the callback was called with the updated buttons
        mock_callback.assert_called_once()

    @patch('evdev.InputDevice')
    @patch('subprocess.Popen')
    def test_setSteeringValues(self, mock_popen, mock_input_device):
        # Create a mock SteeringDeviceConfig
        mock_config = MagicMock(spec=SteeringDeviceConfig)
        mock_config.DeviceVendorID = 1234
        mock_config.ControllerPath = "/dev/input/"

        # Create a mock ButtonsInterface
        mock_buttons = MagicMock(spec=ButtonsInterface)
        mock_config.buttons = mock_buttons

        # Create the SteeringDevice instance with the mock config
        device = SteeringDevice(mock_config)

        # Simulate a button press event
        mock_event = MagicMock(spec=InputEvent)
        mock_event.type = 1  # EV_KEY type
        mock_event.code = 30  # Key code (for example, 'A' button)
        mock_event.value = 1  # Pressed

        # Call the __setSteeringValues method
        updated_buttons = device._SteeringDevice__setSteeringValues(mock_event)

        # Assert the buttons interface was updated (you can assert based on actual behavior)
        self.assertEqual(updated_buttons, mock_buttons)


if __name__ == "__main__":
    unittest.main()
