import unittest
from datetime import datetime
from module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day import app, GREETINGS


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_can_get_correct_username_with_weekdate(self):
        week = 'Хорошей среды'
        current_weekday = datetime.today().weekday()
        expected_greeting = GREETINGS[current_weekday]
        self.assertTrue(week in expected_greeting)

