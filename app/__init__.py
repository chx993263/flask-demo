import datetime
import logging
import os

import xxhash
from logging.config import dictConfig

from flask import Flask
from flask_log_request_id import RequestID, RequestIDLogFilter

from app.config import get_config
from app.extensions import db, redis, mail, login_manager
from app.models import User
from app.web import h5_game


# log config
log_level = 'INFO'
dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'req_id_log_filter': {
            '()': 'flask_log_request_id.RequestIDLogFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(lineno)s] %(name)s: %(message)s'
        },
        'standard-with-req-id': {
            'format': '%(asctime)s [%(request_id)s][%(levelname)s] [%(lineno)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': log_level,
            'formatter': 'standard-with-req-id',
            'filters': ['req_id_log_filter'],
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stdout',  # Default is stderr
        },
        "rotate": {
            'level': log_level,
            'formatter': 'standard-with-req-id',
            'filters': ['req_id_log_filter'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            "filename": "wsgi-rotate.log",
            "when": "D",
            "interval": 1,
            "backupCount": 3
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': log_level,
            'propagate': True
        },
    }
})


def create_app():
    app = Flask(__name__)

    # 加载 app配置
    app.config.from_object(get_config())
    # 注册路由
    # app.register_blueprint(auth_bp)
    app.register_blueprint(h5_game)

    # 注册扩展
    register_extensions(app)

    # 日志
    log_messages(app)

    # reqID.init_app(app) # 在这里不能使用init_app的方式，可能里面的实现没兼容。也可能是我用的方式不对。
    RequestID(app, request_id_parser=empty_id_parser, request_id_generator=id_generator)

    # login_manager.login_view = "auth.login"
    # login_manager.login_message = "please login first"

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    # Initialize extensions/add-ons/plugins.
    db.init_app(app)
    redis.init_app(app)
    # celery.init_app(app)
    mail.init_app(app)
    # login_manager.init_app(app)


class CustomFormatter(logging.Formatter):
    LEVEL_MAP = {logging.FATAL: 'F', logging.ERROR: 'E', logging.WARN: 'W', logging.INFO: 'I', logging.DEBUG: 'D'}

    def format(self, record):
        record.levelletter = self.LEVEL_MAP[record.levelno]
        return super(CustomFormatter, self).format(record)


def empty_id_parser():
    return None


def id_generator():
    x = xxhash.xxh32()
    x.update(os.urandom(20))
    random_str = x.hexdigest()[:4]  # 结果为8位，取前4位

    now = datetime.datetime.utcnow()
    timestr = datetime.datetime.strftime(now, "%m%d-%H%M%S")
    return f'{timestr}-{random_str}'


def log_messages(app):
    """Log messages common to Tornado and devserver."""
    log = logging.getLogger(__name__)
    log.info(app.config)


# 需要提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象。
# 它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return user
