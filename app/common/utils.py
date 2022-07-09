from flask import jsonify, make_response
from flask_log_request_id import current_request_id


def make_result(code: int, msg: str, data: dict):
    jsob = jsonify({'data': data, 'msg': msg, 'status': code,
                   "request_id": current_request_id()})
    resp = make_response(jsob)
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    return resp


def make_text_result(text):
    # 返回纯文本
    resp = make_response(text, 200)
    resp.mimetype = "text/plain"
    resp.headers["Content-Type"] = "text/plain; charset=UTF-8"
    return resp


def make_success_result(data):
    return make_result(200, 'OK', data)
