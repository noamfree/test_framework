"""
written by noam.freeman
"""
from test_framework import *


class WasRun(TestCase):
    def __init__(self, what_to_run):
        self.was_setup = None
        self.was_run = None
        TestCase.__init__(self, what_to_run)

    def testing_method(self):

        self.was_run = True

    def setup(self):
        self.was_setup = True


class TestingTestCase(TestCase):


    def test_was_run(self):
        test = WasRun("testing_method")
        assert test.was_run is None
        test.run()
        assert test.was_run is True

    def test_was_setup(self):
        test = WasRun("testing_method")
        assert test.was_setup == None
        test.run()
        assert  test.was_setup == True

TestingTestCase("test_was_run").run()
TestingTestCase("test_was_setup").run()