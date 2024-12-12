import random
import time
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

@metrics.counter(
    "request_count", "Количество запросов по эндпоинтам",
    labels={"endpoint":lambda:request.endpoint, "method": lambda: request.method}
)
@app.route("/dict")
def test_1():
    time.sleep(1)
    test_list = [1,2,3]
    return jsonify(test_list)

@metrics.counter(
    "hello_request_count", "Количество запросов на /hello/<name>",
    labels={"name":lambda:request.view_args.get('name', 'unknown')}
)
@app.route("/hello/<name>")
def test_2(name):
    time.sleep(1)
    return jsonify({"Hello!":f"{name}"})

@metrics.counter(
    "random_request_count", "Количество запросов на /random"
)
@app.route("/random")
def test_3():
    test_list = []
    time.sleep(1)
    for num in range(3):
        test_list.append(random.randint(1,100))
    return jsonify(test_list)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
