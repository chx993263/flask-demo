#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import IntEnum, Enum


class ResponseStatus(IntEnum):
    Success = 200
    NeedLogin = 401
    NoPermission = 10002
    WrongArguments = 10003
    NotFound = 10004
    ClientType = 10005
    DatabaseOperation = 10006
    UnprocessableEntity = 10022
    UnknowError = 9999

    # Account Related
    CreateAccountFailed = 500
    AccountAlreadyExists = 501
    AccountError = 599  # Default Account Error

    # Budget Related
    CreateBudgetFailed = 601
    UpdateBudgetFailed = 602
    QueryBudgetFailed = 603
    DeleteBudgetFailed = 604

    CaptchaError = 10007