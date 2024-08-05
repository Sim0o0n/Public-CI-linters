# Ошибки и баги person.py

## Ошибка 1: Отсутствует импорт модуля `datetime`
- **Описание**: В исходном коде отсутствует импорт модуля `datetime`, необходимый для работы с датой и временем.
- **Исправление**: Добавить строку `from datetime import datetime` в начало файла.

## Ошибка 2: Метод `get_age`
- **Описание**: Возраст считается как `self.yob - now.year`, что неверно.
- **Исправление**: Должно быть `now.year - self.yob`.

## Ошибка 3: Метод `set_name`
- **Описание**: Метод присваивает имя `self.name` самому себе, вместо использования параметра.
- **Исправление**: Должно быть `self.name = name`.

## Ошибка 4: Метод `set_address`
- **Описание**: Метод использует оператор `==` вместо `=`, что сравнивает значение, а не присваивает его.
- **Исправление**: Должно быть `self.address = address`.

## Ошибка 5: Метод `is_homeless`
- **Описание**: Метод использует несуществующую переменную `address`.
- **Исправление**: Должно быть `self.address`.

## Исправленный person.py:

```python
from datetime import datetime

class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
        self.name: str = name
        self.yob: int = year_of_birth
        self.address: str = address

    def get_age(self) -> int:
        now: datetime = datetime.now()
        return now.year - self.yob

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def set_address(self, address: str) -> None:
        self.address = address

    def get_address(self) -> str:
        return self.address

    def is_homeless(self) -> bool:
        return self.address == ''