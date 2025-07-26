#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
import time
import concurrent.futures

from Runners.ThreadRunner import ThreadRunner


class TestHelper:
    """Helper class for testing ThreadRunner tasks"""
    value = None

    @classmethod
    def store_value(cls, input_value):
        """Store the input value for later verification"""
        cls.value = input_value

    @classmethod
    def clear(cls):
        """Clear the stored value"""
        cls.value = None

    @classmethod
    def get_value(cls):
        """Get the stored value and clear it"""
        value = cls.value
        cls.clear()
        return value


class TestThreadRunner(unittest.TestCase):
    def setUp(self):
        self.runner = ThreadRunner(max_workers=2)
        TestHelper.clear()

    def tearDown(self):
        self.runner.cleanUp()
        TestHelper.clear()

    def test_task_execution(self):
        """Test that tasks are executed and results are properly stored"""
        def task(value):
            TestHelper.store_value(value)

        test_value = "test_value"
        task_id = self.runner.addTask(task, test_value)

        # Give the task time to complete
        time.sleep(0.1)

        # Verify the value was stored correctly
        self.assertEqual(TestHelper.get_value(), test_value)

    def test_multiple_tasks(self):
        """Test that multiple tasks execute in order"""
        def task(value, *args, **kwargs):
            TestHelper.store_value(value)
            return value

        # Launch tasks
        self.runner.addTask(task, "value1")
        time.sleep(0.1)  # Ensure first task completes
        self.assertEqual(TestHelper.get_value(), "value1")

        self.runner.addTask(task, "value2")
        time.sleep(0.1)  # Ensure second task completes
        self.assertEqual(TestHelper.get_value(), "value2")