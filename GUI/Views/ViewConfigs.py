#!/usr/bin/env python3
# @author: Markus Kösters
import tkinter
from dataclasses import dataclass


@dataclass
class RootViewConfig:
    window: tkinter.Tk
    title: str
    geometry: str = '1920x1080'
