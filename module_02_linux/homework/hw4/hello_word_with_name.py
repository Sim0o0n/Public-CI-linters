"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays = (
    "понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья"
)


@app.route('/hello-world/<name>', methods=['GET'])
def hello_world(name):
    weekday_index = datetime.today().weekday()
    greeting = f"Привет, {name}. Хорошей {weekdays[weekday_index]}!"
    return greeting


if __name__ == '__main__':
    app.run(debug=True)
