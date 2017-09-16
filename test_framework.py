from test_status import Failure, Success

TEXT_COLOR = '\033[0m'


class TestResult:
    def __init__(self, what_was_run):
        self.__status = Failure()
        self.what_was_run = what_was_run
        self.error = None

    def __repr__(self, color=True):
        status_message = self.status_message()
        error_message = ("\n" + self.show_problem()) if self.error else ""

        if color:
            status_message = self.__status.color() + status_message + TEXT_COLOR
        return status_message + error_message

    def status_message(self):
        first_line_completion = "-" * len(str(self.__status))
        message_start = "test: "
        second_line_completion = "-" * (len(self.what_was_run) + len(message_start))
        return "[ " + message_start + self.what_was_run + " " + first_line_completion + " ]\n" \
             + "[ " + second_line_completion + " " + str(self.__status) + " ]"

    def status(self):
        return str(self.__status)

    def succeed(self):
        self.__status = Success()

    def fail(self, error):
        self.error = error

    def show_problem(self):
        return type(self.error).__name__ + ": " + str(self.error)


class TestsResult(TestResult):
    def __init__(self, *results):
        self.results = results

    def tests_ran(self):
        return len(self.results)

    def tests_failed(self):
        return len(list(filter(lambda x: x.status() == "FAILURE", self.results)))


class TestCase:
    def __init__(self, what_to_run):
        self.what_to_run = what_to_run

    def run(self) -> TestResult:
        test_result = TestResult(self.what_to_run)

        self.setup()
        try:
            exec("self." + self.what_to_run + "()")
            test_result.succeed()
        except Exception as e:
            test_result.fail(e)
        self.tear_down()

        return test_result

    def setup(self):
        pass

    def tear_down(self):
        pass


class TestSuite(object):
    def __init__(self, *tests):
        self.tests = tests

    def __len__(self):
        return len(self.tests)

    def run(self):
        results = [test.run() for test in self.tests]
        return TestsResult(*results)
