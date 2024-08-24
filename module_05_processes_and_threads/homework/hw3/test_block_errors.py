import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def setUp(self) -> None:
        self.zero_division_error = {ZeroDivisionError}
        self.type_error = {TypeError}

    def test_exception_ignored(self): #Проверяет исключение ZeroDivisionError
        try:
            with BlockErrors(self.zero_division_error):
                a = 1 / 0
        except:
            self.fail("ZeroDivisionError should be ignored")

    def test_exception_propagated(self): # Проверяет исключение TypeError.
        with self.assertRaises(TypeError):
            with BlockErrors(self.zero_division_error):
                a = 1 / '0'


    def test_no_exception(self): #Проверяет, что при отсутствии исключений в блоке with ничего не происходит.
        try:
            with BlockErrors(self.zero_division_error):
                a = 1 + 1
        except:
            self.fail("No exception should occur")


if __name__ == '__main__':
    unittest.main()
