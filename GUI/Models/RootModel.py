#!/usr/bin/env python3
# @author: Markus Kösters

import PIL
import cv2
import numpy
from PIL import ImageTk, Image

import ProjectLogging
from .ModelConfig import ModelConfig


class RootModel:
    """
    Represents a root model for processing image frames and managing related tasks.

    This class provides functionalities to process image frames, convert image formats,
    resize images, and generate predefined images such as a loading screen. The class
    uses an internal runner to execute relevant tasks and ensures compatibility with
    Tkinter by utilizing the ImageTk.PhotoImage format.
    """

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('RootModel',
                                                                      'RootModel.log').getLogger

    def __init__(self, config: ModelConfig):
        self.__config = config

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
        Todo: make resizedFrame and convertedFrame run async and wait for finalization before going on with the tasks
        """
        resizedFrame: numpy.ndarray = self.__resizeFrame(frame)
        convertedFrame: Image = self.__convertFrameFormat(resizedFrame)
        return convertedFrame

    def getLoadingScreen(self) -> ImageTk.PhotoImage:
        """
        Gets the loading screen image.

        This method is used to retrieve the loading screen image pre-loaded as an
        instance property. It returns an image of the type `ImageTk.PhotoImage`.
        This is commonly used in GUI applications to display an initial loading or
        splash screen.

        :return: The loading screen image.
        :rtype: ImageTk.PhotoImage
        """
        return self.__loadingScreen()

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
        return ImageTk.PhotoImage(PIL.Image.fromarray(cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)))

    def __resizeFrame(self, image: numpy.ndarray) -> numpy.ndarray:
        """
        Resize an image to the specified width and height.

        This static method resizes an image to the given dimensions using interpolation
        for optimal scaling. The resized image is return ed as an output for further
        processing or use.

        :param image: The input image to be resized.
        :type image: numpy.ndarray
        :return: A generator return ing the resized image.
        :rtype: numpy.ndarray
        """
        resolution = self.__config.resolution
        self.__logger.debug(f'Resizing frame to: {resolution}')
        return cv2.resize(image, resolution)

    @staticmethod
    def __loadingScreen() -> ImageTk.PhotoImage:
        """
        Creates and returns a loading screen image as an instance of ImageTk.PhotoImage.

        The method generates a blank 1920x1080 image using NumPy, converts it to a
        PIL Image, and draws a "Loading" text at a specified position on the image
        using the PIL ImageDraw module. The text is styled with a bold font loaded
        from the system. The image is finally converted to ImageTk.PhotoImage before
        being returned.

        :raises OSError: When the specified font file cannot be found or loaded.

        :return: A loading screen image with "Loading" text centered and styled in
            bold font.
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
