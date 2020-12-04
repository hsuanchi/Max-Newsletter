# 引用 flask 內建函式
from flask import Flask, g, render_template, request, redirect, url_for

# 引用套件
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_babel import Babel
from celery import Celery

# 引用其他相關模組
import requests
import os

from .config.config import config

celery_redis = config[os.environ.get("FLASK_ENV")].CELERY_BROKER_URL
celery = Celery(__name__, broker=celery_redis, backend=celery_redis)
csrf = CSRFProtect()
jwt = JWTManager()
db = SQLAlchemy()
babel = Babel()
cache = Cache()


def create_app(config_name):
    app = Flask(__name__)

    # 設定config
    app.config.from_object(config[config_name])

    # Initialize Celery
    celery.conf.update(app.config)

    register_extensions(app)
    register_blueprints(app)
    register_celery_beat(celery)
    register_errorhandlers(app)
    register_i18n(app)

    @app.route("/")
    def index_redirect():
        return redirect(url_for("index.article", lang_code="zh"))

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    cache.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    from .views.rss import category
    from .views.index import index
    from .views.email import email

    app.register_blueprint(category, url_prefix="/category")
    app.register_blueprint(index, url_prefix="/<any(zh, en):lang_code>")
    app.register_blueprint(email, url_prefix="/<any(zh, en):lang_code>/email")


def register_errorhandlers(app):
    """Register error handlers with the Flask application."""

    def render_error(e):
        return render_template("errors/%s.html" % e.code, error=e), e.code

    for e in [
        requests.codes.INTERNAL_SERVER_ERROR,
        requests.codes.NOT_FOUND,
        requests.codes.UNAUTHORIZED,
    ]:
        app.errorhandler(e)(render_error)

    @jwt.invalid_token_loader
    def invalid_token_loader(msg):
        """
        參考 https://flask-jwt-extended.readthedocs.io/en/stable/changing_default_behavior/
        """
        return render_template("email/submit_result_fail.html", error=msg), 401


def register_i18n(app):
    """
    參考 https://medium.com/@nicolas_84494/flask-create-a-multilingual-web-application-with-language-specific-urls-5d994344f5fd
    """
    defalut_language_str = app.config["DEFAULT_LANGUAGE"]
    support_language_list = app.config["SUPPORTED_LANGUAGES"]

    # 1 Get parameter lang_code from route
    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop("lang_code", defalut_language_str)
        else:
            g.lang_code = request.path.split("/")[1]

    # 2 Check lang_code type is in config
    @app.before_request
    def ensure_lang_support():
        lang_code = g.get("lang_code", None)
        if lang_code and lang_code not in support_language_list:
            g.lang_code = request.accept_languages.best_match(support_language_list)

    # 3 Setting babel
    @babel.localeselector
    def get_locale():
        return g.get("lang_code")

    # 4 Check lang_pop exist after step1 pop parameter of lang_code
    @app.url_defaults
    def set_language_code(endpoint, values):
        if "lang_code" in values or not g.lang_code:
            return
        if app.url_map.is_endpoint_expecting(endpoint, "lang_code"):
            values["lang_code"] = g.lang_code


def register_celery_beat(celery):
    from .views.celery_tasks import tasks
