class TestStatus:
    def __repr__(self):
        pass

    def color(self):
        pass


class Failure(TestStatus):
    def __repr__(self):
        return "FAILURE"

    def color(self):
        return '\033[91m'


class Success(TestStatus):
    def __repr__(self):
        return "PASSED"

    def color(self):
        return '\033[92m'
