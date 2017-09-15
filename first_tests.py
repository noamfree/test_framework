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


def test_was_run():
    test = WasRun("testing_method")
    print(test.was_run)  # should be None
    test.run()
    print(test.was_run)  # should be True

test_was_run()