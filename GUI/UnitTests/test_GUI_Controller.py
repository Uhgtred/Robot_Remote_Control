#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

import joblib
import numpy

from GUI.GUI_Contoller import GUI_Controller


class TestGUIController(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        self.gui_controller = GUI_Controller()
        print(self.gui_controller)

    def test_updateRootView(self):
        # Now we can test using actual functionality
        imageFrame_rgb = numpy.random.randint(0, 256, (100, 100, 3), numpy.uint8)
        joblib.dump(imageFrame_rgb, "image.pkl")
        with open('image.pkl', 'rb') as file:
            serializedImage = file.read()
        self.gui_controller.updateRootView(serializedImage)


if __name__ == '__main__':
    unittest.main()
