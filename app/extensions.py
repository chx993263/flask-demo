#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Flask and other extensions instantiated here.
To avoid circular imports with views and create_app(), extensions are instantiated here. They will be initialized
(calling init_app()) in application.py.
"""
from logging import getLogger
import os

from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


LOG = getLogger(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
mail = Mail()
redis = FlaskRedis()
login_manager = LoginManager()

cache_tables = {}
