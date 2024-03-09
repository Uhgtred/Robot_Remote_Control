#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

import joblib
import numpy

from GUI.GUI_Contoller import GUI_Controller, ViewProtocol, ModelProtocol
from GUI.Models import ModelFactory
from GUI.Views import ViewFactory


class TestGUIController(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        self.gui_controller = GUI_Controller()
        print(self.gui_controller)

    def test_updateRootView(self):
        # Now we can test using actual functionality
        image = numpy.zeros((10, 10))
        joblib.dump(image, "image.pkl")
        loaded_image = joblib.load("image.pkl")
        self.gui_controller.updateRootView(loaded_image)


if __name__ == '__main__':
    unittest.main()