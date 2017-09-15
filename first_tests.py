"""
written by noam.freeman
"""

# manually confirm running a method
def test_was_run():
    test = WasRun()
    print(test.was_run)  # should be None
    test.testing_method
    print(test.was_run)  # should be True