"""
written by noam.freeman
"""
from test_framework import *


class WasRun(TestCase):
    def __init__(self, what_to_run):
        self.was_run = None
        TestCase.__init__(self, what_to_run)

    def testing_method(self):
        self.was_run = True


class TestingTestCase(TestCase):
    def test_was_run(self):
        test = WasRun("testing_method")
        assert test.was_run is None
        test.run()
        assert test.was_run is True

TestingTestCase("test_was_run").run()