"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

/head_file/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/head_file/12/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""

from flask import Flask, abort, Response
import os

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str):
    abs_path = os.path.abspath(relative_path)

    if not os.path.isfile(abs_path):
        abort(404, description="Файл не найден.")

    result_text = ""
    result_size = 0
    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            result_text = file.read(size)
            result_size = len(result_text)
    except Exception as e:
        abort(500, description="Ошибка при чтении файла.")

    response_text = (
        f"<b>{abs_path}</b> {result_size}<br>"
        f"{result_text}"
    )

    return Response(response_text, content_type='text/html')


if __name__ == "__main__":
    app.run(debug=True)

