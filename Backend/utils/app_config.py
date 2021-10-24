import os
from flask import Flask
from flask import abort, request, jsonify
from functools import wraps
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions


class AppConfig:
    @staticmethod
    def config_app(app):
        if os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True":
            os.environ["DB_URI"] = os.environ["PRODUCTION_DB_URI"]

        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ[
            "SQLALCHEMY_TRACK_MODIFICATIONS"
        ]
        app.config["BUNDLE_ERRORS"] = os.environ["BUNDLE_ERRORS"]

        @app.errorhandler(Exception)
        def handle_error(e):
            code = 500
            if isinstance(e, HTTPException):
                code = e.code
            return jsonify(error=str(e)), code

        for ex in default_exceptions:
            app.register_error_handler(ex, handle_error)

        return app

    @staticmethod
    def get_app_with_db_configured():
        app = Flask(__name__)

        app = AppConfig.config_app(app)
        return app

    @staticmethod
    def require_appkey(view_function):
        # API authentication route decorator
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            print
            if (
                request.args.get("key")
                and request.args.get("key") == os.environ["API_KEY"]
            ):
                return view_function(*args, **kwargs)
            else:
                abort(401)

        return decorated_function
