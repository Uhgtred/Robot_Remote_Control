#!/usr/bin/env python3
# @author: Markus Kösters
import os.path
from pathlib import Path

import cv2
import joblib
import numpy
from PIL import ImageTk, Image

import Runners
from .ModelConfig import ModelConfig


class RootModel:

    def __init__(self, config: ModelConfig):
        self.__rawFrame: bytes = None
        self.__processedFrame: Image = None
        self.__imageFilePath: str = str(Path(os.path.abspath(__file__)).parent) + config.imageFilePath
        self.__runner: Runners = Runners.ThreadRunner()

    def getFrame(self, frame: bytes) -> Image:
        """
        Method for receiving a single video frame.
        :return: Video frame as serialized tkinter PhotoImage.
        """
        self.__runner.addTask(self.__receiveAndProcessNewFrame, frame)
        self.__runner.runTasks()
        if not self.__processedFrame:
            return self.__loadingScreen()
        return self.__converImageFormat(self.__processedFrame)

    def __receiveAndProcessNewFrame(self, frame: bytes) -> None:
        """
        Method that controls how to receive and process new frames.
        """
        self.__storeFrameinFile(frame, self.__imageFilePath)
        self.__processedFrame = self.__deserializeImageFile(self.__imageFilePath)

    def __deserializeImageFile(self, imageFilePath: str) -> numpy.ndarray:
        """
        Method for deserializing an image file.
        :param imageFilePath: File path of the image file that will be deserialized.
        """
        return joblib.load(imageFilePath)

    # Todo: check return-type
    def __converImageFormat(self, imageFrame: numpy.ndarray) -> Image:
        """
        Method for converting the image frame to a format that can be displayed in the GUI (tkinter).
        :param imageFrame: Serialized image frame that will be converted.
        :return:
        """
        return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)))

    def __storeFrameinFile(self, imageData: bytes, imageFilePath: str) -> None:
        """
        Method to store the frame into a file.
        :param imageFilePath: Path in which the image will be stored.
        :param imageData: Data that will be stored in the file.
        """
        with open(imageFilePath, "wb") as file:
            file.write(imageData)

    def __loadingScreen(self):
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
