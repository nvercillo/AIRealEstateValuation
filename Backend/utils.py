import json
import os
from flask import Flask
from sqlalchemy.ext.declarative import DeclarativeMeta
from math import sin, cos, sqrt, atan2, radians, pi
from numpy import arccos
from sqlalchemy.dialects.postgresql import UUID
from flask import abort, request, jsonify
from functools import wraps
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions


class Utils:
    @staticmethod
    def get_app_with_db_configured():
        app = Flask(__name__)

        app = Utils.config_app(app)
        return app

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


class Math:
    def __init__(self):
        self.R = 6373.0  # approximate radius of earth in km

    """ return value is in kms """

    def calc_dist_bw_coords(self, coords1, coords2):
        lat1 = radians(coords1[0])
        lon1 = radians(coords1[1])
        lat2 = radians(coords2[0])
        lon2 = radians(coords2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.R * c

        return distance

    def calc_max_lon_deviance(self, d):
        lon2 = arccos(-2 * pow(sin(d / (2 * self.R)), 2) + 1)

        lon2 = lon2 * 180 / pi  # convert back to degrees
        return lon2

    def calc_max_lat_deviance(self, d, lat1):
        lat1 = radians(lat1)

        lat2 = arccos(-2 * pow(sin(d / (2 * self.R)), 2) / pow(cos(lat1), 2) + 1)

        lat2 = lat2 * 180 / pi  # convert back to degreees
        return lat2

    def mode(self, _list):
        _list.sort()

        mode = None
        count = 0

        l_mode = None
        l_count = 0

        for l in _list:
            if l != l_mode:
                if l_mode is not None and l_count > count:
                    count = l_count
                    mode = l_mode

                l_mode = l
                l_count = 1
            else:
                l_count += 1
        if l_mode is not None and l_count > count:
            count = l_count
            mode = l_mode

        return mode


class AlchemyEncoder(json.JSONEncoder):
    """Purpose of this class is to facilitate the json serializability of sql
    alchemy queries"""

    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex

        if isinstance(obj.__class__, DeclarativeMeta):

            if isinstance(obj, UUID):
                # if the obj is uuid, we simply return the value of uuid
                return obj.hex

            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex

        if isinstance(obj.__class__, DeclarativeMeta):

            if isinstance(obj, UUID):
                # if the obj is uuid, we simply return the value of uuid
                return obj.hex

            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
