"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask, abort

app = Flask(__name__)


@app.route("/max_number/<path:numbers>", methods=['GET'])
def max_number(numbers):
    numbers_list = numbers.split('/')

    try:
        numbers_list = [int(num) for num in numbers_list]
    except ValueError:
        abort(400, description="Все параметры должны быть целыми числами.")

    max_number = max(numbers_list)

    response = f"Максимальное переданное число <i>{max_number}</i>"

    return response


if __name__ == "__main__":
    app.run(debug=True)

