#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass


@dataclass
class VideoControllerConfig:
    filePath = '/VideoData/robotImage.pkl'