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
from flask import request, abort

load_dotenv(join(dirname(__file__), ".env"))

app = Utils.get_app_with_db_configured()

from models import db  # this line needs to be after app assignment

from controllers import enumerations_controller
from controllers import properties_controller
from controllers import ai_model_controller
from controllers import image_controller

EnumerationsController = enumerations_controller.EnumerationsController
PropertiesController = properties_controller.PropertiesController
AIModelController = ai_model_controller.AIModelController
ImageController = image_controller.ImageController

""" ROUTES """

@app.route("/")
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def welcome_text():
    # if not (request.args.get("key") and request.args.get("key") == os.environ["API_KEY"]): abort(401)
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


@app.route("/api/property_images_ids", methods=["GET"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey
def get_image_ids_for_property():

    property_id = request.args.get("property_id")
    ids = ImageController().get_images_ids_for_property(property_id)

    if len(ids) == 0:  # no images for property
        ids = [ImageController.INVALID_IMAGE_ID]

    response = app.response_class(
        response=json.dumps(ids, cls=AlchemyEncoder),
        status=200,
        mimetype="application/json",
    )

    return response


# TODO: Implement w DB images
@app.route("/api/property_images", methods=["GET"])
@cross_origin(supports_credentials=True)
@Utils.require_appkey 
def get_property_image_from_id():
    
    image_id = request.args.get("image_id")
    raw_image_binary = ImageController().get_image_by_id(image_id)
    
    response = app.response_class(
        response=raw_image_binary,
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


db.init_app(app)

if __name__ == "__main__":
    if os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True":
        print("\nStarted production server .... :)\n")
        print("APP URL: https://localhost:5000\n")
        print(f"Production DB URI: {os.environ['DB_URI']}")
        app.run(debug=True)  # run default flask server
        # serve(app, host="0.0.0.0", port=5000)  # run production server
    else:
        app.run(debug=True)  # run default flask server
