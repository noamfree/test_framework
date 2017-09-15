class TestResult:
    def __init__(self, what_was_run):
        self.status = "FAILURE"
        self.what_was_run = what_was_run

    def __repr__(self):
        first_line_completion = "-" * len(self.status)
        message_start = "test: "
        second_line_completion = "-" * (len(self.what_was_run) + len(message_start))
        return "[ " + message_start + self.what_was_run + " " + first_line_completion + " ]\n" \
               + "[ " + second_line_completion + " " + self.status + " ]"

    def succeed(self):
        self.status = "PASSED"

    def fail(self, error):
        self.error = error

    def show_problem(self):
        return type(self.error).__name__ + ": " + str(self.error)



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
