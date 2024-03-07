#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass


@dataclass
class ViewConfig:
    title: str
    width: int
    height: int
