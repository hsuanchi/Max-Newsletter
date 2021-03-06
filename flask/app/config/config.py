import os
from datetime import timedelta
import datetime
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # Session
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_QUERY_STRING_NAME = "jwt_token"
    JWT_TOKEN_LOCATION = ["query_string", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # 多國語系
    BABEL_TRANSLATION_DIRECTORIES = "translations"
    SUPPORTED_LANGUAGES = ["zh", "en"]
    DEFAULT_LANGUAGE = "zh"

    # Celery
    CELERY_TIMEZONE = "Asia/Taipei"


class DevelopmentConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_ECHO = True

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("db")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_timeout": 900,
        "pool_size": 10,
        "max_overflow": 5,
    }

    # Cache
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    # Other
    HOST_NAME = "http://127.0.0.1:5000"


class ProductionConfig(BaseConfig):
    DEBUG = False

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("db")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_timeout": 900,
        "pool_size": 10,
        "max_overflow": 5,
    }

    # Cache
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
    CELERY_BROKER_URL = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND = "redis://redis:6379/2"

    # Celery bet
    CELERYBEAT_SCHEDULE = {
        "crawler_all_everyday": {
            "task": "crawler_all_everyday",
            "schedule": crontab(minute=15, hour=7),
        },
        "clean_data_everyday": {
            "task": "clean_data_everyday",
            "schedule": crontab(minute=15, hour=8),
        },
        "send_admin_mail_task": {
            "task": "send_admin_mail_task",
            "schedule": crontab(minute=0, hour=9),
        },
        "send_week_mail_task": {
            "task": "send_week_mail_task",
            "schedule": crontab(minute=0, hour=16, day_of_week="thu"),
        },
    }

    # Other
    HOST_NAME = "https://article.maxlist.xyz"


class TestingConfig(BaseConfig):
    TESTING = True

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

    # 關閉 CSRF
    WTF_CSRF_ENABLED = False

    # For testing and/or development only
    CELERY_BROKER_URL = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND = "redis://redis:6379/2"
    # default debugging port of celery 4.4.7 is 6900 according to official
    # doc, however the port differs very often and CELERY_RDB_PORT does not
    # take effect
    #
    # in my case it is usally 6906, and then 6907
    # CELERY_RDB_PORT = 6900

    # Other
    HOST_NAME = "http://127.0.0.1:5000"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
