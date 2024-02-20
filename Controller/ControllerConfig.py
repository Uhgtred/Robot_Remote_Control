#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass


@dataclass
class ControllerConfig:
    ControllerPath = '/dev/input/'
    DeviceVendorID = 12068
    LXAxis = 0  # leftmost value=-32768 rightmost value=32767
    LYAxis = 1  # upmost value=-32768 downmost value=32767
    LTrigger = 2  # max value=255
    LBtn = 310
    L3 = 317
    RXAxis = 3  # leftmost value=-32768 rightmost value=32767
    RYAxis = 4  # upmost value=-32768 downmost value=32767
    RTrigger = 5  # max value=255
    RBtn = 311
    R3 = 318
    StartBtn = 315
    SelectBtn = 314
    ABtn = 304
    BBtn = 305
    XBtn = 307
    YBtn = 308
    XCross = 16  # left value=-1 right value=1
    YCross = 17