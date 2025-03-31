#!/usr/bin/env python3
# @author: Markus Kösters
import os.path
from pathlib import Path

import cv2
import numpy
from PIL import ImageTk, Image

import Runners
from .ModelConfig import ModelConfig


class RootModel:
    """
    Represents a root model for processing image frames and managing related tasks.

    This class provides functionalities to process image frames, convert image formats,
    resize images, and generate predefined images such as a loading screen. The class
    uses an internal runner to execute relevant tasks and ensures compatibility with
    Tkinter by utilizing the ImageTk.PhotoImage format.

    :ivar __imageFilePath: The file path to the image resource, derived from configuration.
    :type __imageFilePath: str
    :ivar __runner: The runner instance used to manage task execution.
    :type __runner: Runners
    """
    def __init__(self, config: ModelConfig):
        self.__imageFilePath: str = str(Path(os.path.abspath(__file__)).parent) + config.imageFilePath
        self.__runner: Runners = Runners.ThreadRunner()

    def getFrame(self, frame: numpy.ndarray) -> Image:
        """
        Processes a given frame and converts it into a specific image format.

        This method takes a NumPy array representing an image frame, executes related
        tasks, and then converts and returns the processed image.

        :param frame: The input image frame.
        :type frame: numpy.ndarray
        :return: The processed image in a specific format.
        :rtype: Image
        """
        """
        Todo: Dataclass or class representing a frame.
        """
        self.__runner.runTasks()
        resizedFrame: Image = self.__resizeFrame(frame, 1920, 1080)
        convertedFrame: Image = self.__convertFrameFormat(resizedFrame)
        return convertedFrame

    @staticmethod
    def __loadingScreen():
        """
        Generates a loading screen image with the text "Loading" displayed in the center.
        The image is created as a 1920x1080 black canvas, with the text rendered in blue
        color using a specified font.

        This static method utilizes the PIL library for image manipulation and rendering.

        :rtype: ImageTk.PhotoImage
        :return: A PhotoImage instance created from the image with "Loading" text.
        """
        """
        Todo: This should probably be a dataclass or class.
        """
        from PIL import Image, ImageTk, ImageFont, ImageDraw

        # Create a NumPy array representing an image of size 1920x1080 with all black pixels
        img_array = numpy.zeros((1080, 1920), dtype=numpy.uint8)

        # Convert the NumPy array to a PIL Image object
        image_pil = Image.fromarray(img_array)

        # Create ImageDraw object
        draw = ImageDraw.Draw(image_pil)

        # Load a font (you might need to adapt path to a font file accordingly)
        # The size 70 refers to the font size
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 70)

        # Define the text and its properties
        text = "Loading"
        # textwidth, textheight = font.size(text)
        # Set the position for the text to be at the center of image
        # position = ((image_pil.width - textwidth) / 2, (image_pil.height - textheight) / 2)

        # Add text to image
        draw.text((0, 0), text, font=font, fill="blue")

        # Convert the PIL image to an ImageTk.PhotoImage
        return ImageTk.PhotoImage(image_pil)
