import unittest
from datetime import datetime
from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person_name_user = Person(name='John', year_of_birth=2000, address='234 Main str')
        self.person_name_user_absent_address = Person(name='Maria', year_of_birth=2001)

    def test_get_name(self):
        self.assertEqual(self.person_name_user.get_name(), 'John')
        self.assertEqual(self.person_name_user_absent_address.get_name(), 'Maria')

    def test_set_name(self):
        self.person_name_user.set_name('Jimmy')
        self.assertEqual(self.person_name_user.get_name(), 'Jimmy')

    def test_get_age(self):
        correct_year = datetime.now().year
        year_olds = correct_year - 2000
        self.assertEqual(self.person_name_user.get_age(), year_olds)

    def test_get_address(self):
        self.assertEqual(self.person_name_user.get_address(), '234 Main str')

    def test_set_address(self):
        self.person_name_user.set_address('534 Old str')
        self.assertEqual(self.person_name_user.get_address(), '534 Old str')

    def test_is_homeless(self):
        self.assertTrue(self.person_name_user_absent_address.is_homeless())
        self.assertFalse(self.person_name_user.is_homeless())


if __name__ == '__main__':
    unittest.main()
