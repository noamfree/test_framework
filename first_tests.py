"""
written by noam.freeman
"""
from test_framework import *


class WasRun(TestCase):
    def __init__(self, what_to_run):
        self.log = ""
        self.was_setup = None
        self.was_run = None
        TestCase.__init__(self, what_to_run)

    def testing_method(self):
        self.log += "running: %s " % self.what_to_run
        self.was_run = True

    def setup(self):
        self.log += "setup "
        self.was_setup = True

    def tear_down(self):
        self.log += "teardown "


class TestingTestCase(TestCase):
    def test_setup_run_teardown_order(self):
        test = WasRun("testing_method")
        assert test.log == ""
        test.run()
        assert test.log == "setup running: testing_method teardown "

    def test_report_succeeding_test(self):
        test = WasRun("testing_method")
        test_result = test.run()
        assert test_result.status == "PASSED"
        assert str(test_result) == "[ test: testing_method ------ ]\n" \
                                   "[ -------------------- PASSED ]"

print(TestingTestCase("test_setup_run_teardown_order").run())
print(TestingTestCase("test_report_succeeding_test").run())
