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


class BrokenTest(TestCase):
    def broken_method(self):
        raise Exception("FOO!!!!")


class TestingTestCase(TestCase):
    def setup(self):
        self.working_test = WasRun("testing_method")
        self.broken_test = BrokenTest("broken_method")

    def test_setup_run_teardown_order(self):
        assert self.working_test.log == ""
        self.working_test.run()
        assert self.working_test.log == "setup running: testing_method teardown "

    def test_report_succeeding_test(self):
        test_result = self.working_test.run()
        assert test_result.status() == "PASSED"
        assert test_result.__repr__(color=False) == "[ test: testing_method ------ ]\n" \
                                   "[ -------------------- PASSED ]"

    def test_report_success_with_color(self):
        test_result = self.working_test.run()
        assert test_result.status() == "PASSED"
        assert str(test_result) == "\033[92m" \
                                   "[ test: testing_method ------ ]\n" \
                                   "[ -------------------- PASSED ]\033[0m"

    def test_reporting_failure(self):
        test_result = self.broken_test.run()
        assert test_result.status() == "FAILURE"

    def test_report_what_is_the_problem(self):
        test_result = self.broken_test.run()
        assert test_result.show_problem() == "Exception: FOO!!!!"
        assert test_result.__repr__(color=False) == "[ test: broken_method ------- ]\n" \
                                   "[ ------------------- FAILURE ]\n" \
                                   "Exception: FOO!!!!"

    def test_report_fail_with_color(self):
        test_result = self.broken_test.run()
        assert test_result.show_problem() == "Exception: FOO!!!!"
        assert str(test_result) == "\033[91m" \
                                   "[ test: broken_method ------- ]\n" \
                                   "[ ------------------- FAILURE ]\033[0m\n" \
                                   "Exception: FOO!!!!"

    def test_suite(self):
        suite = TestSuite(self.working_test, self.broken_test)
        assert len(suite) == 2


    def test_running_suite(self):
        suite = TestSuite(self.working_test, self.broken_test, self.broken_test)
        suite_result = suite.run()
        assert suite_result.tests_ran() == 3
        assert suite_result.tests_failed() == 2

    # def test_reporting_succesful_suite(self):
    #     suite = TestSuite(self.working_test, self.working_test)
    #     suite_result = suite.run()
    #



print(TestingTestCase("test_setup_run_teardown_order").run())
print(TestingTestCase("test_report_succeeding_test").run())
print(TestingTestCase("test_reporting_failure").run())
print(TestingTestCase("test_report_what_is_the_problem").run())
print(TestingTestCase("test_report_success_with_color").run())
print(TestingTestCase("test_report_fail_with_color").run())
print(TestingTestCase("test_suite").run())
print(TestingTestCase("test_running_suite").run())

