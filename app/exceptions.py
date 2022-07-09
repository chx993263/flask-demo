#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.common.constants import ResponseStatus
from app.common import error_formatter


class BaseAppException(Exception):
    status_code = 200
    msg = ""
    error_code = 9999

    def __init__(self, msg=None, status_code=None, error_code=None, payload=None):
        super().__init__(msg)
        if msg:
            self.msg = msg
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['msg'] = self.msg
        rv['status'] = self.error_code
        return rv


class NeedLoginException(BaseAppException):
    code = 200
    msg = 'need login'
    error_code = ResponseStatus.NeedLogin.value


class NoPermissionException(BaseAppException):
    code = 200
    msg = 'invalid permissions'
    error_code = ResponseStatus.NoPermission.value


class WrongArgumentsException(BaseAppException):
    code = 200
    msg = 'invalid argument'
    error_code = ResponseStatus.WrongArguments.value


class NotFoundException(BaseAppException):
    code = 200
    msg = 'the resource are not found O__O...'
    error_code = ResponseStatus.NotFound.value


class ClientTypeError(BaseAppException):
    code = 200
    msg = 'client is invalid'
    error_code = ResponseStatus.ClientType.value


class ServerError(BaseAppException):
    code = 200
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = ResponseStatus.UnknowError.value


class DatabaseOperationException(BaseAppException):
    code = 200
    msg = "database operate exception"
    error_code = ResponseStatus.DatabaseOperation.value


class AccountException(BaseAppException) :
    code = 200
    msg = "account operation error"
    error_code = ResponseStatus.AccountError


class IllegalParamException(Exception):
    """
    参数校验错误异常
    """
    code = 600

    def __init__(self, msg, code=600, **kwargs):
        super().__init__(msg, **kwargs)
        self.code = code


class ProNameException(Exception):
    """
    for full ProName err code list, check error_msg.csv
    """
    def __init__(self, msg, code=-1, **kwargs):
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.msg_detail = kwargs

    def __str__(self):
        error_info = error_formatter.find_and_format_error(
            self.msg, apl_code=self.code, need_formated=False,
            msg_detail=self.msg_detail)
        if error_info is not None:
            self.code = error_info['apl_code']
            msg = error_formatter.format_msg(error_info)
            return msg
        else:
            return (
                f'[ProName Error]: {self.code}, {self.msg} '
            )
