import os
import json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from functools import wraps
from utils import Utils, AlchemyEncoder
from dotenv import load_dotenv
from os.path import join, dirname
from waitress import serve
from flask import request


load_dotenv(join(dirname(__file__), ".env"))

app = Utils.get_app_with_db_configured()

from models import Property  # this line needs to be after app assignment

from controllers import enumerations_controller
from controllers import properties_controller
from controllers import ai_model_controller

EnumerationsController = enumerations_controller.EnumerationsController
PropertiesController = properties_controller.PropertiesController
AIModelController = ai_model_controller.AIModelController

""" ROUTES """


@app.route("/")
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def welcome_text():
    return "This is an authenticated server :)"


@app.route("/api/adjacent_nodes", methods=["POST"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def get_adjacent_nodes():

    req = json.loads(request.data)

    data, five_nearest_ids = PropertiesController()._get_adjacent_nodes(
        req["lng"], req["lat"]
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
        response=json.dumps({"nodes": data, "predicted_price": predicted_price}),
        status=200,
        mimetype="application/json",
    )

    return response


@app.route("/api/amenities", methods=["GET"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def get_amenities_from_id():

    requested_id = request.args.get("id")

    prop = PropertiesController()._get_by_id(requested_id)

    response = app.response_class(
        response=json.dumps(prop, cls=AlchemyEncoder),
        status=200,
        mimetype="application/json",
    )

    return response


@app.route("/api/enumerations", methods=["GET"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def get_enumations():

    data = EnumerationsController.get_all()
    response = app.response_class(
        response=json.dumps(data), status=200, mimetype="application/json"
    )
    return response


@app.route("/api/get_cities_and_sample_addresses", methods=["GET"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def get_list_of_serviced_cities():

    locations = {
        "toronto": ["67 Bond Street", "100 King Street", "100 University Ave West"],
        "calgary": ["340 8 Ave SW", "100 7 Ave SW", "312 12 Ave SW"],
    }

    response = app.response_class(
        response=json.dumps(locations, cls=AlchemyEncoder),
        status=200,
        mimetype="application/json",
    )

    return response


if __name__ == "__main__":
    if os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True":
        print("Started production server .... :)")
        print(f"Production DB URI: {os.environ['DB_URI']}")
        serve(app, host="0.0.0.0", port=5000)  # run production server
    else:
        app.run(debug=True)  # run default flask server
