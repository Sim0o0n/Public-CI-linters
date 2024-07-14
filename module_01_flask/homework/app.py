import datetime
from datetime import datetime, timedelta
from flask import Flask
import random
import os
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')


@app.route('/hello_world')
def test_function_1():
    return 'Hello world!'


@app.route('/cars')
def test_function_2():
    list_cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']
    return ', '.join(list_cars)


@app.route('/cats')
def test_function_3():
    list_cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
    return random.choice(list_cats)


@app.route('/get_time/now')
def test_function_4():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def test_function_5():
    current_time = datetime.now()
    time_delta = timedelta(hours=1, minutes=20, seconds=45)
    future_time = current_time + time_delta
    current_time_after_hour = future_time.strftime("%Y-%m-%d %H:%M:%S")
    return f'Точное время через 1 час 20 минут и 45 секунд: {current_time_after_hour}'


with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    text = book.read()

words = re.findall(r'\b\w+\b', text)


@app.route('/get_random_word')
def test_function_6():
    random_word = random.choice(words)
    return f'Случайное слово: {random_word}'


counter = 0


@app.route('/counter')
def test_function_7():
    global counter
    counter += 1
    return f'Страница была открыта {counter} раз(а)'


if __name__ == '__main__':
    app.run(debug=True)
