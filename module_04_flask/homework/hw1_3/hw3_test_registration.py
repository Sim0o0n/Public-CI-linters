"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import RegistrationForm


valid_data = {
    'email': 'test@example.com',
    'phone': 1234567890,
    'name': 'John Doe',
    'address': '123 Main St',
    'index': 12345,
    'comments': 'No comments'
}


class RegistrationFormTestCase(unittest.TestCase):
    def test_valid_data(self):
        form = RegistrationForm(data=valid_data)
        self.assertTrue(form.validate())

    def test_invalid_email(self):
        invalid_data = valid_data.copy()
        invalid_data['email'] = 'invalid_email'
        form = RegistrationForm(data=invalid_data)
        self.assertFalse(form.validate())
        self.assertIn(form.errors)

    def test_invalid_phone(self):
        invalid_data = valid_data.copy()
        invalid_data['phone'] = 895
        form = RegistrationForm(data=invalid_data)
        self.assertFalse(form.validate())
        self.assertIn('phone', form.errors)

    def test_empty_name(self):
        invalid_data = valid_data.copy()
        invalid_data['name'] = ''
        form = RegistrationForm(data=invalid_data)
        self.assertFalse(form.validate())
        self.assertIn('name', form.errors)

    def test_empty_index(self):
        invalid_data = valid_data.copy()
        invalid_data['invalid'] = ''
        form = RegistrationForm(data=invalid_data)
        self.assertFalse(form.validate())
        self.assertIn('index', form.errors)

    def test_empty_comments(self):
        invalid_data = valid_data.copy()
        invalid_data['comments'] = ''
        form = RegistrationForm(data=invalid_data)
        self.assertFalse(form.validate())
        self.assertIn('comments', form.errors)


if __name__ == '__main__':
    unittest.main()
