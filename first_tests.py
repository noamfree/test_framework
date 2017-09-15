"""
written by noam.freeman
"""

# manually confirm running a method
class WasRun:
    def __init__(self):
        self.was_run = None

    def testing_method(self):
        self.was_run = True


def test_was_run():
    test = WasRun()
    print(test.was_run)  # should be None
    test.testing_method()
    print(test.was_run)  # should be True

test_was_run()