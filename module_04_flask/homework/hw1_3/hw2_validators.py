"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    message = message or f"Число должно содержать от {min} до {max} цифр."

    def _number_length(form, field):
        number_length = len(str(abs(field.data)))
        if number_length < min or number_length > max:
            raise ValidationError(message)

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if not self.min <= (len(str(field.data))) <= self.max:
            raise ValidationError(self.message)

