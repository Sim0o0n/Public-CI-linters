"""
В этом файле будет ваше Flask-приложение
"""

from flask import Flask, request, jsonify
from module_22_celery.homework.task import process_image_and_send_email
from module_22_celery.homework.shared import subscribers
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery_app = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

@app.route("/blur", methods=["POST"])
def blur_images():
    data = request.json
    images = data.get('image')
    email = data.get('receiver_email')

    task = process_image_and_send_email.delay(images, email)
    return jsonify({"task_id": task.id}), 202

@app.route("/status/<task_id>", methods=["GET"])
def progress_and_status(task_id):
    task = celery_app.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'progress': 0,
            'result': None
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'progress': task.info.get('progress', 0),
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
            'progress': 0,
            'result': str(task.info)
        }

    return jsonify(response)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get('email')
    if email in subscribers:
        return jsonify({"message": "Вы уже подписаны."}), 400

    subscribers[email] = True
    return jsonify({"message": "Вы успешно подписались."}), 201

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.json
    email = data.get('email')

    if email not in subscribers:
        return jsonify({"message": "Вы не подписаны."}), 400

    del subscribers[email]
    return jsonify({"message": "Вы успешно отписались."}), 200

if __name__ == "__main__":
    app.run(debug=True)
