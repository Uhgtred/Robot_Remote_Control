#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ButtonData(Protocol):
    # Defining the attributes of a single button.
    ID: int
    value: int


@dataclass
class ButtonsInterface(Protocol):
    buttonData: ButtonData

    @property
    def getButtonDict(self) -> dict:
        """
        Interface-Method for the process-method of a Buttons-object.
        :return:
        """