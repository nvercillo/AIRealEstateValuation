import os
import json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from flask_cors import CORS, cross_origin
from functools import wraps
from waitress import serve
from utils import Utils, AlchemyEncoder
from flask import (
    jsonify, 
    Response, 
    request, 
    has_request_context, 
    make_response, 
    Flask, 
    abort
)
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))


''' SERVER INITIALIZATION AND CONFIG '''

app = Utils.get_app_with_db_configured()
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# API authentication route decorator
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == os.environ['API_KEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


''' allows cross origin communication '''
CORS(app, support_credentials=True)
db = SQLAlchemy(app)
''' END SERVER INITIALIZATION AND CONFIG '''

''' Models DO NOT REMOVE THESE LINES ''' 
from models import Property # used this line used to migrate table


''' Controllers ''' 
from controllers import enumerations_controller
EnumerationsController = enumerations_controller.EnumerationsController
from controllers import properties_controller
PropertiesController = properties_controller.PropertiesController
from controllers import ai_model_controller
AIModelController = ai_model_controller.AIModelController 


''' ROUTES '''
@app.route("/")
@cross_origin(supports_credentials=True)
def welcome_text():
    return "This is an authenticated server :)"


@app.route("/api/adjacent_nodes", methods=["POST"])
@cross_origin(supports_credentials=True)
@require_appkey
def get_adjacent_nodes():
    req = json.loads(request.data)

    data, five_nearest_ids = PropertiesController()._get_adjacent_nodes(
        req['lng'],
        req['lat']
    )
    
    community, district = PropertiesController()._get_community_data_from_nearest(
        five_nearest_ids
    )

    predicted_price = AIModelController().dummy_predict_price()
    
    # predicted_price = AIModelController().predict_price([
    #     # req['lng'],
    #     # req['lat'],
    #     req['Sqaurefootage'],
    #     req['Type'],
    #     req['Style'],
    #     community,
    #     district.split(" ")[1],
    #     req['Bedrooms'],
    #     req['Dens'],
    #     req['Bathrooms'],
    #     req['ParkingTotal']
    # ])

    response = app.response_class(
        response=json.dumps(
            {
                "nodes" : data,
                "predicted_price" : predicted_price 
            }
        ),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route("/api/amenities", methods=["GET"])
@cross_origin(supports_credentials=True)
@require_appkey
def get_amenities_from_id():
    
    requested_id = request.args.get("id")
    
    prop = PropertiesController()._get_by_id(
        requested_id
    )

    response = app.response_class(
        response=json.dumps(prop, cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route("/api/enumerations", methods=["GET"])
@cross_origin(supports_credentials=True)
@require_appkey
def get_enumations():

    data = EnumerationsController.get_all()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return data

''' END ROUTES '''


''' INSTANTIATE SERVER '''
if __name__ == '__main__':
    if os.environ['PRODUCTION'] and os.environ['PRODUCTION'] == "True":
        print(os.environ['DB_URI'])
        print("Started production server .... :)")
        serve(app, host="0.0.0.0", port=5000) # run production server
    else: 
        app.run(debug=True)   # run default flask server 

''' END START UP SERVER '''