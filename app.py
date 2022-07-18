import os
from typing import Iterator, Any, List

from flask_restx import Api, abort, Resource
from flask import Flask, request, Response
import re


app = Flask(__name__)
api = Api(app)
my_ns = api.namespace("perform_query")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def create_query(it: Iterator, cmd: str, value: str) -> List[Any]:
    res = list(map(lambda x: x.strip(), it))
    if cmd == "filter":
        res = list(filter(lambda x: value in x, res))
        return res
    if cmd =="sort":
        res = list(sorted(res, reverse=bool(value)))
        return res
    if cmd == "unique":
        res = list(set(res))
        return res
    if cmd == "limit":
        res = list(res)[: int(value)]
        return res
    if cmd == "map":
        res = list(map(lambda x: x.split(" ")[int(value)], res))
        return res
    if cmd == "regex":
        regex = re.compile(value)
        res = list(filter(lambda x: regex.search(x), it))
        return res
    return []



@my_ns.route("/")
class QueryView(Resource):
    def get(self) -> Response:
        try:
            cmd_1 = request.args["cmd_1"]
            cmd_2 = request.args["cmd_2"]
            val_1 = request.args["val_1"]
            val_2 = request.args["val_2"]
            file_name = request.args["file_name"]
        except Exception:
            abort(400, message="invalid query")
        path_file = os.path.join(DATA_DIR, str(file_name))
        if not os.path.exists(path_file):
            abort(400, message="file not found")

        with open(path_file) as f:
            result = create_query(iter(f), str(cmd_1), str(val_1))
            if cmd_2 and val_2:
                result = create_query(iter(result), str(cmd_2), str(val_2))

        return app.response_class("\n".join(result), content_type="text/plain")


if __name__ == "__main__":
    app.run(debug=False)