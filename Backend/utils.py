import json 
import os
from flask import Flask
from sqlalchemy.ext.declarative import DeclarativeMeta

class Utils:
    @staticmethod
    def get_app_with_db_configured():
        app = Flask(__name__)

        app = Utils.config_app(app)
        return app
    
 
    @staticmethod
    def config_app(app):
        if os.environ['PRODUCTION'] and os.environ['PRODUCTION'] == "True":
            os.environ["DB_URI"] = os.environ['PRODUCTION_DB_URI']
        
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
        app.config['BUNDLE_ERRORS'] = os.environ['BUNDLE_ERRORS']
        return app


class AlchemyEncoder(json.JSONEncoder):
    ''' Purpose of this class is to facilitate the json serializability of sql 
    alchemy queries '''
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)