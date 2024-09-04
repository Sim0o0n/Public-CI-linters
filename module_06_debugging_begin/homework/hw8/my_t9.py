"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import re
from typing import List, Dict

digit_to_letters: Dict[str, str] = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}

def load_english_words(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file]

def my_t9(input_numbers: str) -> List[str]:
    english_words = load_english_words('/usr/share/dict/words')
    regex_pattern = ''.join([f"[{digit_to_letters[digit]}]" for digit in input_numbers])
    pattern = re.compile(f"^{regex_pattern}$")
    matching_words = [word for word in english_words if pattern.match(word)]
    return matching_words


if __name__ == '__main__':
    try:
        numbers: str = input("Введите цифры от 2 до 9: ")
        if not re.match("^[2-9]+$", numbers):
            raise ValueError("Некорректный ввод! Пожалуйста, введите только цифры от 2 до 9.")
        words: List[str] = my_t9(numbers)
        print("Подходящие слова:")
        print(*words, sep='\n')
    except Exception as e:
        print(f"Ошибка: {e}")