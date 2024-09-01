#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass, field

from SteeringInput.ButtonsInterface import ButtonsInterface


@dataclass
class ButtonData:
    # Defining the style of a button.
    ID: int
    value: int


@dataclass
class ButtonsXBox:
    LXAxis: ButtonData = field(default_factory=lambda: ButtonData(0, 0))  # leftmost value: ButtonData = ButtonDef(-32768 rightmost value: ButtonData = ButtonDef(32767
    LYAxis: ButtonData = field(default_factory=lambda: ButtonData(1, 0))  # upmost value: ButtonData = ButtonDef(-32768 downmost value: ButtonData = ButtonDef(32767
    LTrigger: ButtonData = field(default_factory=lambda: ButtonData(2, 0))  # max value: ButtonData = ButtonDef(255
    LBtn: ButtonData = field(default_factory=lambda: ButtonData(310, 0))
    L3: ButtonData = field(default_factory=lambda: ButtonData(317, 0))
    RXAxis: ButtonData = field(default_factory=lambda: ButtonData(3, 0))  # leftmost value: ButtonData = ButtonDef(-32768 rightmost value: ButtonData = ButtonDef(32767
    RYAxis: ButtonData = field(default_factory=lambda: ButtonData(4, 0))  # upmost value: ButtonData = ButtonDef(-32768 downmost value: ButtonData = ButtonDef(32767
    RTrigger: ButtonData = field(default_factory=lambda: ButtonData(5, 0))  # max value: ButtonData = ButtonDef(255
    RBtn: ButtonData = field(default_factory=lambda: ButtonData(311, 0))
    R3: ButtonData = field(default_factory=lambda: ButtonData(318, 0))
    StartBtn: ButtonData = field(default_factory=lambda: ButtonData(315, 0))
    SelectBtn: ButtonData = field(default_factory=lambda: ButtonData(314, 0))
    ABtn: ButtonData = field(default_factory=lambda: ButtonData(304, 0))
    BBtn: ButtonData = field(default_factory=lambda: ButtonData(305, 0))
    XBtn: ButtonData = field(default_factory=lambda: ButtonData(307, 0))
    YBtn: ButtonData = field(default_factory=lambda: ButtonData(308, 0))
    XCross: ButtonData = field(default_factory=lambda: ButtonData(16, 0))  # left value: ButtonData = ButtonDef(-1 right value: ButtonData = ButtonDef(1
    YCross: ButtonData = field(default_factory=lambda: ButtonData(17, 0))

    @property
    def getButtonDict(self) -> dict:
        return {
            self.LXAxis.ID: self.LXAxis.value,
            self.LYAxis.ID: self.LYAxis.value,
            self.LTrigger.ID: self.LTrigger.value if not self.LBtn.value else -self.LTrigger.value,
            self.L3.ID: self.L3.value,
            self.RXAxis.ID: self.RXAxis.value,
            self.RYAxis.ID: self.RYAxis.value,
            self.RTrigger.ID: self.RTrigger.value if not self.RBtn.value else -self.RTrigger.value,
            self.R3.ID: self.R3.value,
            self.StartBtn.ID: self.StartBtn.value,
            self.SelectBtn.ID: self.SelectBtn.value,
            self.ABtn.ID: self.ABtn.value,
            self.BBtn.ID: self.BBtn.value,
            self.XBtn.ID: self.XBtn.value,
            self.YBtn.ID: self.YBtn.value,
            self.XCross.ID: self.XCross.value,
            self.YCross.ID: self.YCross.value,
        }


@dataclass
class SteeringDeviceConfig:
    # defining the default configuration of a controller!
    ControllerPath: str = '/dev/input/'
    DeviceVendorID: int = 1118
    buttons: ButtonsInterface = field(default_factory=ButtonsXBox)

