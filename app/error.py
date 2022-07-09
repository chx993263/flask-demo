#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify
from logging import getLogger

from app.common.utils import make_result
from app.exceptions import BaseAppException, IllegalParamException

logger = getLogger(__name__)


def handle_invalid_usage(error):
    if isinstance(error, BaseAppException):
        logger.exception('error: %s', error)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        response.headers["Content-Type"] = "application/json; charset=UTF-8"
        return response

    elif isinstance(error, IllegalParamException):
        return make_result(error.code, str(error), {})
    else:
        logger.exception('error: %s' % error)
        # response = jsonify({'msg': 'sorry, we made a mistake (*￣︶￣)!', 'status': 500}), 200
        # response = jsonify({'msg': str(error), 'status': 500}), 200
        return make_result(500, str(error), {})

    # return response


def handle_unprocessable_entity(err):
    logger.exception(err)

    exc = getattr(err, "exc")
    if exc:
        # messages = exc.messages
        messages = str(exc.messages)
    else:
        messages = "Invalid request"
    # return jsonify({"msg": messages}), 422
    # return jsonify({"msg": messages, "status": 10022}), 200
    return make_result(10022, messages, {})


def handle_not_found(e):
    # return jsonify({"msg": str(e), "status": 404}), 200
    return make_result(404, str(e), {})


def handle_unauthorized(e):
    # return jsonify({"msg": str(e), "status": 401}), 200
    return make_result(401, str(e), {})


def handle_forbidden(e):
    # return jsonify({"msg": str(e), "status": 403}), 200
    return make_result(403, str(e), {})


def init_error_handlers(*kwargs):
    for it in kwargs:
        it.app_errorhandler(Exception)(handle_invalid_usage)
        it.app_errorhandler(401)(handle_unauthorized)
        it.app_errorhandler(403)(handle_forbidden)
        it.app_errorhandler(404)(handle_not_found)
        it.app_errorhandler(422)(handle_unprocessable_entity)
