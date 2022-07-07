import os

from flask import Flask,request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
# получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат

def create_query(it, cmd, value):
    res = map(lambda x: x.strip(), it)
    if cmd == "filter":
        res = filter(lambda x: value in x, res)
    if cmd =="sort":
        # value = bool(value)
        res = sorted(res, reverse=value)
    if cmd == "unique":
        res = set(res)
    if cmd == "limit":
        value = int(value)
        res = list(res)[: value]
    if cmd == "map":
        value = int(value)
        res = map(lambda x: x.split(" ")[value], res)
    return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd_1 = request.args["cmd_1"]
        cmd_2 = request.args["cmd_2"]
        val_1 = request.args["val_1"]
        val_2 = request.args["val_2"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest
    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest

    with open(path_file) as f:
        result = create_query(f, cmd_1, val_1)
        result = create_query(result, cmd_2, val_2)
        result = "\n".join(result)

    return app.response_class(result, content_type="text/plain")
