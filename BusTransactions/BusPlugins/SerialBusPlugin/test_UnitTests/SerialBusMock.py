#!/usr/bin/env python3
# @author: Markus Kösters

class MockSerialBus:
    buffer = []
    state = False

    def read(self):
        if self.buffer:
            return self.buffer.pop(0)

    @classmethod
    def write(cls, message):
        cls.buffer.append(message)

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

    def __str__(self):
        """
        Mock implementation of a serial communication bus as a string representation.
        This method is intended to provide a human-readable string equivalent for
        the MockSerialBus object.

        :return: A string representation of the MockSerialBus class.
        :rtype: str
        """
        return 'MockSerialBus'