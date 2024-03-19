# import unittest
# from unittest.mock import patch, Mock
# import evdev
#
# from SteeringInput import SteeringDevice
# from SteeringInput.SteeringDeviceConfig import SteeringDeviceConfig
#
#
# class test_SteeringDevice(unittest.TestCase):
#
#     def setUp(self):
#         config = SteeringDeviceConfig()
#         # initialize your config object here
#         self.steering_device = SteeringDevice(config)
#
#     @patch("evdev.InputDevice")
#     def test_set_steering_values(self, MockInputDevice):
#         """Test the _setSteeringValues method."""
#
#         mocked_event = MockInputDevice.return_value
#
#         output = self.steering_device._SteeringDevice__setSteeringValues(mocked_event)
#         # assert the state of the `config.buttons` after function call
#
#     @patch("subprocess.Popen")
#     @patch("evdev.InputDevice")
#     def test_init_controller(self, MockInputDevice, MockPopen):
#         """Test the __initController method."""
#
#         MockPopen.return_value.communicate.return_value = ("sample_device_listing", None)
#         MockInputDevice.return_value.info.vendor = 7711  # use your own vendorID
#
#         self.steering_device._SteeringDevice__initController(7711)
#         # assert the state / existence of the `__controller` attribute after function call
#
#     @patch("evdev.InputDevice")
#     def test_read_controller(self, MockInputDevice):
#         """Test the readController method."""
#
#         MockInputDevice.return_value.read_loop.return_value = []
#         some_method = lambda x: x
#
#         self.steering_device.readController(some_method)
#         # assert that `some_method` has been called with the expected argument
#
#
# if __name__ == "__main__":
#     unittest.main()
