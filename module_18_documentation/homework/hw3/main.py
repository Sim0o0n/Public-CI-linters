import operator
from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Сложение двух чисел.

    :param a: Первое число.
    :param b: Второе число.

    Пример запроса для сложения:
    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:
    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    return operator.add(a, b)


@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    """
    Вычитание двух чисел.

    :param a: Первое число.
    :param b: Второе число.

    Пример запроса для вычитания:
    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.subtract",
            "params": {"a": 10, "b": 3},
            "id": "2"
        }' http://localhost:5000/api

    Пример ответа:
    {
      "id": "2",
      "jsonrpc": "2.0",
      "result": 7
    }
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
    Умножение двух чисел.

    :param a: Первое число.
    :param b: Второе число.

    Пример запроса для умножения:
    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.multiply",
            "params": {"a": 4, "b": 5},
            "id": "3"
        }' http://localhost:5000/api

    Пример ответа:
    {
      "id": "3",
      "jsonrpc": "2.0",
      "result": 20
    }
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    """
    Деление двух чисел.

    :param a: Делимое.
    :param b: Делитель.

    Пример запроса для деления:
    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.divide",
            "params": {"a": 10, "b": 2},
            "id": "4"
        }' http://localhost:5000/api

    Пример ответа:
    {
      "id": "4",
      "jsonrpc": "2.0",
      "result": 5
    }

    Если b равно 0, то возвращается ошибка:
    {
      "jsonrpc": "2.0",
      "error": {
          "code": -32602,
          "message": "Division by zero is not allowed."
      },
      "id": null
    }
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return operator.truediv(a, b)


@app.errorhandler(ValueError)
def handle_value_error(error):
    response = {
        "jsonrpc": "2.0",
        "error": {
            "code": -32602,
            "message": str(error),
        },
        "id": None
    }
    return response, 400


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

