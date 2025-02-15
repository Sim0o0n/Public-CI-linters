import unittest
from remote_execution import app
import unittest
import json
from flask import Flask

class CodeExecutionTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_successful_execution(self):
        code = "print('Hello, World!')"
        timeout = 5
        response = self.app.post('/run_code', json={'code': code, 'timeout': timeout})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'], 'Hello, World!')

    def test_timeout(self):
        code = """
    import time
    time.sleep(10)
    print('This will not be printed if timeout is too short.')
    """
        timeout = 1
        response = self.app.post('/run_code', json={'code': code, 'timeout': timeout})
        self.assertEqual(response.status_code, 408)
        self.assertIn("Code execution timed out", json.loads(response.data)['error'])

    def test_invalid_timeout(self):
        code = "print('Hello, World!')"
        timeout = 7
        response = self.app.post('/run_code', json={'code': code, 'timeout': timeout})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid timeout value", json.loads(response.data)['error'])

    def test_no_code(self):
        timeout = 5
        response = self.app.post('/run_code', json={'timeout': timeout})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No code provided", json.loads(response.data)['error'])

    def test_invalid_code(self):
        code = "print(Hello, World!)"
        timeout = 5
        response = self.app.post('/run_code', json={'code': code, 'timeout': timeout})
        self.assertEqual(response.status_code, 500)
        self.assertIn("SyntaxError", json.loads(response.data)['error'])

if __name__ == '__main__':
    unittest.main()
