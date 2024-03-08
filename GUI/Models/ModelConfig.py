#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass

import BusTransactions


@dataclass
class ModelConfig:
    imageFilePath = '/VideoData/robotImage.pkl'
