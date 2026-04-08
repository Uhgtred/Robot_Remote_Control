#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ButtonsProtocol(Protocol):

    @property
    def getButtonDict(self) -> dict:
        """
        Interface-Method for the process-method of a Buttons-object.
        :return:
        """
