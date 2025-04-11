#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass, field
from email.policy import default

import BusTransactions


@dataclass
class ModelConfig:
    """
    Dataclass used as a configuration for the RootModel.
    """
    resolution: list[int] = field(default_factory = lambda: [1920, 1080])
