class TestCase:
    def __init__(self, what_to_run):
        self.what_to_run = what_to_run

    def run(self):
        self.setup()
        exec("self." + self.what_to_run + "()")

    def setup(self):
        pass