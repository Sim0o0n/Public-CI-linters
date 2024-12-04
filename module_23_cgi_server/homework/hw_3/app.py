from flask import Flask
import time

app = Flask(__name__)


@app.route('/long_task')
def long_task():
    time.sleep(300)
    return "Task completed!"


