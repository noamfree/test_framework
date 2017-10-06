"""
written by noam.freeman
"""
import traceback

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
    # noinspection PyAttributeOutsideInit
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
        assert str(test_result).startswith("\033[92m")  # green color
        assert str(test_result).endswith("\033[0m")  # back to regular color

    def test_reporting_failure(self):
        test_result = self.broken_test.run()
        assert test_result.status() == "FAILURE"

    def test_report_what_is_the_problem(self):
        test_result = self.broken_test.run()
        assert test_result.show_problem() == "Exception: FOO!!!!"
        assert "Exception: FOO!!!!" in test_result.__repr__(color=False)

    def test_print_trace_of_problem(self):
        test_result = self.broken_test.run()
        assert test_result.error.trace == "trace"

    def test_report_fail_with_color(self):
        test_result = self.broken_test.run()
        assert test_result.show_problem() == "Exception: FOO!!!!"
        assert str(test_result).startswith("\033[91m")  # red color
        assert "\033[0m" in str(test_result)  # back to regular color

    def test_suite(self):
        suite = TestSuite("suite", self.working_test, self.broken_test)
        assert len(suite) == 2

    def test_running_suite(self):
        suite = TestSuite("suite", self.working_test, self.broken_test, self.broken_test)
        suite_result = suite.run()
        assert suite_result.tests_ran() == 3
        assert suite_result.tests_failed() == 2

    def test_reporting_successful_suite(self):
        suite = TestSuite("suite", self.working_test, self.working_test)
        suite_result = suite.run()
        assert suite_result.__repr__(color=False) == "[ test: suite ------ ]\n" \
                                                     "[ ----------- PASSED ]"

    def test_reporting_failed_suite(self):
        suite = TestSuite("suite", self.working_test, self.broken_test)
        suite_result = suite.run()
        assert "[ test: suite ------- ]\n" \
               "[ ----------- FAILURE ]" in str(suite_result)
        assert str(self.working_test.run()) in str(suite_result)
        assert str(self.broken_test.run()) in str(suite_result)



print(TestingTestCase("test_setup_run_teardown_order").run())

basic_test_suite = TestSuite("test_testing",
                             TestingTestCase("test_report_succeeding_test"),
                             TestingTestCase("test_reporting_failure"),
                             TestingTestCase("test_report_what_is_the_problem"),
                             TestingTestCase("test_report_success_with_color"),
                             TestingTestCase("test_report_fail_with_color"),
                             # TestingTestCase("test_print_trace_of_problem"),
                             )

suite_test_suite = TestSuite("suite_testing",
                             TestingTestCase("test_suite"),
                             TestingTestCase("test_running_suite"),
                             TestingTestCase("test_reporting_successful_suite"),
                             TestingTestCase("test_reporting_failed_suite"),
                             )
print(basic_test_suite.run())
print(suite_test_suite.run())


