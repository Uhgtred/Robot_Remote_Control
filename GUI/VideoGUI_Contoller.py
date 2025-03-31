#!/usr/bin/env python3
# @author: Markus Kösters

import atexit
import tkinter
import cv2
import numpy
from PIL import ImageTk, Image

import ProjectLogging
from .Models import ModelFactory
from .Models.ModelProtocol import ModelProtocol
from .Views import ViewFactory
from .Views.ViewProtocol import ViewProtocol


class VideoGUI_Controller:
    """
    Controller class for managing the video GUI application.

    This class is responsible for initializing the main components of the GUI,
    including the root window, view, and model. It also controls the main event
    loop for the GUI and updates the view based on the model's current state.

    :ivar __rootWindow: The main Tkinter root window for the application.
    :type __rootWindow: tkinter.Tk
    :ivar __rootView: The root view of the application, created via a view factory.
    :type __rootView: ViewProtocol
    :ivar __rootModel: The root model of the application, created via a model factory.
    :type __rootModel: ModelProtocol
    """

    __rootWindow: tkinter.Tk = None
    __rootView: ViewProtocol = None
    __rootModel: ModelProtocol = None

    def __init__(self):
        self.__rootWindow: tkinter.Tk = tkinter.Tk()
        self.__rootView: ViewProtocol = ViewFactory.produceRootView(self.__rootWindow)
        self.__rootModel: ModelProtocol = ModelFactory.produceRootModel()
        # Initializing a logger. The loglevel can globally be set in 'ProjectLogging.Logger'.
        self.__logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('VideoGUI_Controller',
                                                                     'VideoGUI_Controller.log').getLogger
        atexit.register(self.__rootWindow.destroy)

    def runMainLoop(self) -> None:
        """
        Executes the main event loop for the application.

        This method starts the Tkinter main loop by invoking the
        `mainloop` method on the root window. The call to `mainloop` is
        blocking and will keep the application running until the main
        loop is terminated. Typically, this loop enables the GUI to
        listen for events and update widgets accordingly.

        :raises RuntimeError: If the main loop fails to execute or is
                               interrupted unexpectedly.
        """
        self.__rootWindow.mainloop()

    @staticmethod
    def __convertFrameFormat(imageFrame: numpy.ndarray) -> Image:
        """
        Converts an image frame from a NumPy array in BGR color format to an image in RGB
        format, suitable for Tkinter integration.

        :param imageFrame: A NumPy ndarray representing the image frame in BGR color format.
        :type imageFrame: numpy.ndarray
        :return: A PhotoImage object compatible with Tkinter, converted from the input image.
        :rtype: ImageTk.PhotoImage
        """
        return ImageTk.PhotoImage(tkinter.Image.fromarray(cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)))

    @staticmethod
    def __resizeFrame(image: Image, width: int, height: int) -> Image:
        """
        Resize an image to the specified width and height.

        This static method resizes an image to the given dimensions using interpolation
        for optimal scaling. The resized image is return ed as an output for further
        processing or use.

        :param image: The input image to be resized.
        :type image: Image
        :param width: The target width for the resized image.
        :type width: int
        :param height: The target height for the resized image.
        :type height: int
        :return: A generator return ing the resized image.
        :rtype: Image
        """
        return cv2.resize(image, (width, height))

    def updateRootView(self, frame: bytes) -> None:
        """
        Updates the root view with the given frame data.

        This method updates the root view component by fetching the processed
        frame data from the root model using the provided frame, and passing it
        to the root view. The update ensures the view reflects the latest state
        derived from the provided frame.

        :param frame: The binary data representing a frame that is to be processed
            and reflected in the root view.
        """
        self.__logger.debug(f'Updating root view with frame: {type(frame)}\n of size: {len(frame)}')
        frame: Image = self.__rootModel.getFrame(frame)
        resizeFrame: Image = self.__resizeFrame(frame, 1920, 1080)
        convertedFrame: Image = self.__convertFrameFormat(resizeFrame)
        self.__rootView.updateFrame(convertedFrame)
