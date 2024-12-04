import json


from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/hello")
def say_hello():
    return json.dumps({"response":"Hello,World!"})


@app.route("/hello/<name>")
def say_hello_with_name(name:str):
    return json.dumps({"response":f"Hello,{name}!"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error":"not_found"}), 404


if __name__ == "__main__":
    app.run(debug=True)