"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask, jsonify, abort

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])

    if number < 0:
        abort(400, description="Сумма расхода не может быть отрицательной.")

    if year not in storage:
        storage[year] = {'total': 0, 'months': {}}

    if month not in storage[year]['months']:
        storage[year]['months'][month] = {'total': 0, 'days': {}}

    if day not in storage[year]['months'][month]['days']:
        storage[year]['months'][month]['days'][day] = 0

    storage[year]['months'][month]['days'][day] += number
    storage[year]['months'][month]['total'] += number
    storage[year]['total'] += number

    return jsonify({"message": "Расход добавлен"}), 200


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    if year not in storage:
        return jsonify({"total": 0}), 200

    return jsonify({"total": storage[year]['total']}), 200


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if year not in storage or month not in storage[year]['months']:
        return jsonify({"total": 0}), 200

    return jsonify({"total": storage[year]['months'][month]['total']}), 200


if __name__ == "__main__":
    app.run(debug=True)

