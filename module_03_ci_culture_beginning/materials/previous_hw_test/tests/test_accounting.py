import unittest
from module_02_linux.homework.hw7.accounting import app, storage


class TestFinancialApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        storage.update({
            2024: {
                'total': 1000,
                'months': {
                    8: {'total': 500, 'days': {1: 100, 2: 150, 3: 250}},
                    9: {'total': 500, 'days': {10: 200, 11: 300}}
                }
            }
        })

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_add_valid_data(self):
        response = self.client.get('/add/20240815/200')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Расход добавлен"})
        self.assertEqual(storage[2024]['months'][8]['days'][15], 200)

    def test_add_negative_number(self):
        response = self.client.get('/add/20240815/-100')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Сумма расхода не может быть отрицательной.", response.data.decode())

    def test_add_invalid_date(self):
        response = self.client.get('/add/20241332/50')
        self.assertEqual(response.status_code, 404)

    def test_calculate_year(self):
        response = self.client.get('/calculate/2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"total": 1000})

    def test_calculate_month(self):
        response = self.client.get('/calculate/2024/8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"total": 500})

    def test_calculate_empty_storage(self):
        storage.clear()
        response = self.client.get('/calculate/2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"total": 0})


if __name__ == '__main__':
    unittest.main()
