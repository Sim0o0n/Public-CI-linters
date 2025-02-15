import json
from flask import Flask, request


app = Flask(__name__)
logs_storage = []

@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    try:
        log_record = request.get_json()
        logs_storage.append(log_record)
        return "Log received", 200
    except Exception as e:
        return f"Failed to process log: {str(e)}", 400


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    return '<pre>' + json.dumps(logs_storage, indent=4) + '</pre>', 200


if __name__ == '__main__':
    app.run(debug=True)