from test_status import Failure, Success




class TestResult:
    def __init__(self, what_was_run):
        self._status = Failure()
        self.what_was_run = what_was_run
        self.error = None

    def __repr__(self, color=True):
        status_message = self.status_message()
        error_message = ("\n" + self.show_problem()) if self.error else ""

        if color:
            status_message = self._status.color_text(status_message)
        return status_message + error_message

    def status_message(self):
        first_line_completion = "-" * len(str(self._status))
        message_start = "test: "
        second_line_completion = "-" * (len(self.what_was_run) + len(message_start))
        return "[ " + message_start + self.what_was_run + " " + first_line_completion + " ]\n" \
             + "[ " + second_line_completion + " " + self.status() + " ]"

    def status(self):
        return str(self._status)

    def succeed(self):
        self._status = Success()

    def fail(self, error):
        self.error = error

    def show_problem(self):
        return type(self.error).__name__ + ": " + str(self.error)


class TestsResult(TestResult):
    def __init__(self, what_was_run,  *results):
        TestResult.__init__(self, what_was_run)
        self.results = []
        self._status = Success()

    def tests_ran(self):
        return len(self.results)

    def tests_failed(self):
        return len(list(filter(lambda x: x.status() == "FAILURE", self.results)))

    def add_results(self, *results):
        for result in results:
            self.results.append(result)
        self.update_status()

    def update_status(self):
        if self.tests_failed():
            self._status = Failure()

    def __repr__(self, color=True):
        suite_repr = TestResult.__repr__(self, color)
        tests_repr = ("\n" + self.tests_repr(color)) if self.tests_failed() else ""
        return suite_repr + tests_repr

    def tests_repr(self, color):
        tests_reprs = []
        for i, result in enumerate(self.results):
            tests_reprs.append("test " + str(i+1) + ":")
            tests_reprs.append(result.__repr__(color))
        tests_reprs = "\n".join(tests_reprs)
        return tests_reprs


class TestCase:
    def __init__(self, what_to_run):
        self.what_to_run = what_to_run
        self.init_results()

    def run(self) -> TestResult:
        self.setup()

        try:
            self.running_command()
        except Exception as e:
            self.test_result.fail(e)

        self.tear_down()

        return self.test_result

    def init_results(self):
        self.test_result = TestResult(self.what_to_run)

    def running_command(self):
        exec("self." + self.what_to_run + "()")
        self.test_result.succeed()

    def setup(self):
        pass

    def tear_down(self):
        pass


class TestSuite(TestCase):
    def __init__(self, name,  *tests):
        self.name = name
        super().__init__(name)
        self.tests = tests

    def __len__(self):
        return len(self.tests)

    def init_results(self):
        self.test_result = TestsResult(self.name)

    def running_command(self):
         self.test_result.add_results(*[test.run() for test in self.tests])
         # self.test_result.add_results(*[test.run().set_name(self.name + "::" + get_name()) for test in self.tests])


