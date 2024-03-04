#!/usr/bin/env python3
# @author: Markus Kösters
import threading
import time
import unittest

from Runners import ThreadRunner


def testTask(*args):
    # print(f"Testing {args}")
    time.sleep(1)


def test2Task():
    time.sleep(1)


class test_ThreadRunner(unittest.TestCase):
    testRunner = ThreadRunner()

    def test_addTasks(self):
        self.testRunner.addTask(testTask, ['test', 'test2'])
        self.assertIn('testTask_thread', (task.name for task in self.testRunner._ThreadRunner__threads))
        self.testRunner.addTask(test2Task)
        self.assertEqual(len(self.testRunner._ThreadRunner__threads), 2)

    def test_runTasks(self):
        self.testRunner.addTask(test2Task)
        thread = self.testRunner._ThreadRunner__threads[0]
        self.testRunner.runTasks()
        self.assertEqual(len(self.testRunner._ThreadRunner__threads), 0)
        self.assertTrue(thread.is_alive())
        time.sleep(2)
        self.assertFalse(thread.is_alive())


if __name__ == '__main__':
    unittest.main()
