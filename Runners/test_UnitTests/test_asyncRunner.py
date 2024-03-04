#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from Runners.asyncRunner import AsyncRunner


def test1(sleepTime):
    # print('test from 1')
    time.sleep(sleepTime)
    # print('end from 1')


def test2(sleepTime):
    # print('test from 2')
    time.sleep(sleepTime)
    # print('end from 2')


def test(sleepTime):
    # print('test from 0')
    time.sleep(sleepTime)
    # print('end from 0')


class test_AsyncRunner(unittest.TestCase):
    obj = AsyncRunner()

    def test_addTask(self):
        self.obj.addTask(test, 1)
        self.obj.addTask(test2, 2)
        self.assertEqual(len(self.obj._AsyncRunner__tasks), 2)
        self.obj._AsyncRunner__tasks.clear()

    def test_runTask(self):
        start = time.time()
        times = [.1, .2, .3]
        self.obj.addTask(test, times[2])
        self.obj.addTask(test1, times[1])
        self.obj.addTask(test2, times[0])
        self.obj.runTasks()
        stop = time.time() - start
        self.assertEqual(round(stop, 1), max(times))


if __name__ == '__main__':
    unittest.main()
