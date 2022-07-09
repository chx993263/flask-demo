import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)


class Config:
    DEBUG = False
    HOST = "127.0.0.1"
    LISTEN_HOST = "0.0.0.0"
    LISTEN_PORT = 12345
    SECRET_KEY = "abcdefg"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_POOL_SIZE = 200
    # SQLALCHEMY_POOL_RECYCLE = 6000
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True, 'pool_size': 200, 'pool_timeout': 30, 'pool_recycle': 60
    }

    _SQLALCHEMY_DATABASE_DATABASE = ''
    _SQLALCHEMY_DATABASE_HOSTNAME = ''
    _SQLALCHEMY_DATABASE_PORT = 3306
    _SQLALCHEMY_DATABASE_USERNAME = ''
    _SQLALCHEMY_DATABASE_PASSWORD = ''

    _SQLALCHEMY_DATABASE_CHARSET = 'utf8mb4'

    SQLALCHEMY_DATABASE_URI = property(
        lambda self: 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'.format(
            user=self._SQLALCHEMY_DATABASE_USERNAME,
            password=self._SQLALCHEMY_DATABASE_PASSWORD,
            host=self._SQLALCHEMY_DATABASE_HOSTNAME,
            port=self._SQLALCHEMY_DATABASE_PORT,
            db=self._SQLALCHEMY_DATABASE_DATABASE,
            charset=self._SQLALCHEMY_DATABASE_CHARSET
        ))


def get_config(config_name=None):
    config = Config()
    return config
