TEXT_COLOR = '\033[0m'

class TestStatus:
    def __repr__(self):
        pass

    def color(self):
        pass

    def color_text(self, text):
        return self.color() + text + TEXT_COLOR


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
