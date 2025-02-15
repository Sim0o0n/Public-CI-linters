"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess
from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField


app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField()
    timeout = IntegerField()


def run_python_code_in_subproccess(code: str, timeout: int):
    with open('temp_code.py', 'w') as file:
        file.write(code)

    command = ['python3', 'temp_code.py']

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return {"result": stdout.strip(), "stderr": stderr.strip()}

        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return {"error": "Code execution timed out", "stdout": stdout.strip(), "stderr": stderr.strip()}

    except Exception as e:
        return {"error": str(e)}



@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')
    timeout = data.get('timeout', 5)

    result = run_python_code_in_subproccess(code, timeout)

    if 'error' in result:
        if result['error'] == 'Code execution timed out':
            return jsonify(result), 408
        else:
            return jsonify(result), 500
    else:
        return jsonify({"result": result['result']}), 200


if __name__ == '__main__':
    app.run(debug=True)

