import unittest
from redirect import Redirect
import sys
import io

class TestRedirect(unittest.TestCase):
    def setUp(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def test_redirect_stdout(self):
        with Redirect(stdout=self.stdout):
            print("Hello stdout")
        self.assertEqual(self.stdout.getvalue(), "Hello stdout\n")

    def test_redirect_stderr(self):
        with Redirect(stderr=self.stderr):
            print("Hello stderr", file=sys.stderr)
        self.assertEqual(self.stderr.getvalue(), "Hello stderr\n")

    def test_redirect_stdout_and_stderr(self):
        with Redirect(stdout=self.stdout, stderr=self.stderr):
            print("Hello stdout", file=sys.stdout)
            print("Hello stderr", file=sys.stderr)
        self.assertEqual(self.stdout.getvalue(), "Hello stdout\n")
        self.assertEqual(self.stderr.getvalue(), "Hello stderr\n")

    def test_no_redirect(self):
        with Redirect():
            print("This should go to the original stdout")
            print("This should go to the original stderr", file=sys.stderr)
        self.assertEqual(self.stdout.getvalue(), "")
        self.assertEqual(self.stderr.getvalue(), "")


if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
