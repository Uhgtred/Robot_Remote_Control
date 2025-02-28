#!/usr/bin/env python3
# @author: AI

import ProjectLogging
from SteeringInput.SteeringDeviceConfig import SteeringDeviceConfig


class SteeringDeviceStub:
    """
    A class representing a Steering Device interface.

    This class provides methods to interact with and control a steering device.
    It includes initialization, device search, vendor identification, and reading control inputs.
    """

    def __init__(self, config: SteeringDeviceConfig):
        """
        Initializes the SteeringDevice with a given configuration.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        self.__conf: SteeringDeviceConfig = config  # Mock configuration
        self.__controller = "MockController"  # Mock controller as a string
        self.__logger = ProjectLogging.Logger('SteeringDeviceStub', 'SteeringDeviceStub.log').getLogger

    def __setSteeringValues(self, values):
        """
        Mock method to set the steering values for the device.

        Args:
            values (dict): A dictionary containing steering values (e.g., angle, speed).

        Returns:
            bool: True to simulate successful setting of steering values.
        """
        if not isinstance(values, dict):
            raise ValueError("Steering values must be provided as a dictionary.")
        self.__logger.debug(f"Steering values set to: {values}")  # Mock behavior
        return True

    def initController(self):
        """
        Mock method to initialize the controller for the steering device.

        Returns:
            bool: True to simulate successful controller initialization.
        """
        self.__logger.debug(f"Controller '{self.__controller}' initialized with config: {self.__conf}")
        return True

    def __checkVendorID(self, vendor_id):
        """
        Mock private method to check if the vendor ID matches a known valid ID.

        Args:
            vendor_id (str): Vendor ID to be checked.

        Returns:
            bool: True if the Vendor ID is valid, False otherwise.
        """
        self.__logger.debug(self.__conf)
        valid_vendor_id_from_config = self.__conf.DeviceVendorID # Mock valid vendor IDs
        is_valid = vendor_id == valid_vendor_id_from_config
        self.__logger.debug(f"Vendor ID '{vendor_id}' check: {'Valid' if is_valid else 'Invalid'}, expected: {valid_vendor_id_from_config}")
        return is_valid

    def __searchAvailableDevices(self):
        """
        Mock method to search for all available steering devices connected to the system.

        Returns:
            list: A list of mock available steering devices' details.
        """
        devices = [
            {"id": "device1", "type": "Steering Device A", "status": "connected"},
            {"id": "device2", "type": "Steering Device B", "status": "connected"}
        ]  # Mocked list of devices
        self.__logger.debug("Available devices:", devices)
        return devices

    def readController(self):
        """
        Mock method to read inputs from the controller and process them.

        Returns:
            dict: Mock details about the controller's current state (e.g., axis position, button state).
        """
        controller_state = {
            "axis_x": 0.5,  # Mock X-axis position (steering angle, normalized between -1 and 1)
            "axis_y": 0.0,  # Mock Y-axis position (e.g., throttle, normalized between -1 and 1)
            "buttons": {"A": False, "B": True},  # Mock button states
        }
        self.__logger.debug(f"Controller state: {controller_state}")
        return controller_state