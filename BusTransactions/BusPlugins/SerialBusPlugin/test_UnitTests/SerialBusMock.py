#!/usr/bin/env python3
# @author: Markus Kösters

class MockSerialBus:
    buffer = []
    state = False

    def read(self):
        if self.buffer:
            return self.buffer.pop(0)

    def write(self, message):
        self.buffer.append(message)

    @classmethod
    def is_open(cls):
        return cls.state

    def open(self):
        self.state = True

    def close(self):
        self.state = False

    @property
    def getBuffer(self):
        return self.buffer
