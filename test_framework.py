class TestResult:
    def __init__(self, what_was_run):
        self.status = "PASSED"
        self.what_was_run = what_was_run

    def __repr__(self):

        first_line_completion = "-" * len(self.status)
        message_start = "test: "
        second_line_completion = "-" * (len(self.what_was_run) + len(message_start))
        return "[ " + message_start + self.what_was_run + " " + first_line_completion + " ]\n" \
             + "[ " + second_line_completion +            " " + self.status +                " ]"


class TestCase:
    def __init__(self, what_to_run):
        self.what_to_run = what_to_run

    def run(self) -> TestResult:
        self.setup()
        exec("self." + self.what_to_run + "()")
        self.tear_down()
        return TestResult(self.what_to_run)

    def setup(self):
        pass

    def tear_down(self):
        pass
