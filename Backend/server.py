from math import ceil
import os
import json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from dotenv import load_dotenv
from os.path import join, dirname
from waitress import serve
from flask import request, abort
from utils.app_config import AppConfig
from utils.encoders import AlchemyEncoder
from utils.data_structures.image_cache import ImageCache

load_dotenv(join(dirname(__file__), ".env"))

image_cache = ImageCache(capacity=3)  # 10 images big + default
app = AppConfig.get_app_with_db_configured()

from models import db  # this line needs to be after app assignment

from controllers.enumerations_controller import EnumerationsController
from controllers.properties_controller import PropertiesController
from controllers.ai_model_controller import AIModelController
from controllers.image_controller import ImageController


image_controller = ImageController()
property_controller = PropertiesController()
ai_model_controller = AIModelController()

""" ROUTES """


@app.route("/")
@cross_origin(supports_credentials=True)
# @AppConfig.require_appkey
def welcome_text():
    return "This is an authenticated server :)"


index = 0


@app.route("/test_cache")
@cross_origin(supports_credentials=True)
# @AppConfig.require_appkey
def test_cache():
    global index
    image_cache.put(index, 0)
    index += 1
    return str(image_cache)


@app.route("/api/adjacent_nodes", methods=["POST"])
@cross_origin(supports_credentials=True)
@AppConfig.require_appkey
def get_adjacent_nodes():

    req = json.loads(request.data)

    data, five_nearest_ids = property_controller._get_adjacent_nodes(
        req["lng"], req["lat"]
    )

    # community, district = property_controller._get_community_data_from_nearest(
    #     five_nearest_ids
    # )

    predicted_price = ai_model_controller.dummy_predict_price()

    # predicted_price = ai_model_controller.predict_price([
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
@AppConfig.require_appkey
def get_amenities_from_id():

    requested_property_id = request.args.get("id")

    prop = property_controller._get_by_id(requested_property_id)
    if prop:
        response = app.response_class(
            response=prop.data,
            status=200,
            mimetype="application/json",
        )
    else:
        response = app.response_class(
            response=f'Property id: "{requested_property_id}" not in database',
            status=400,
            mimetype="application/json",
        )

    return response


@app.route("/api/property_images_ids", methods=["GET"])
@cross_origin(supports_credentials=True)
@AppConfig.require_appkey
def get_image_ids_for_property():

    property_id = request.args.get("property_id")
    arr = image_controller.get_images_ids_for_property(property_id)

    if len(arr) == 0:  # no images for property
        arr = [[ImageController.INVALID_IMAGE_ID, ImageController.INVALID_IMAGE_LEN]]

    arr = [[e[0], ceil(int(e[1]) / ImageController.INVALID_IMAGE_LEN)] for e in arr]

    response = app.response_class(
        response=json.dumps(arr, cls=AlchemyEncoder),
        status=200,
        mimetype="application/json",
    )

    return response


@app.route("/api/property_images", methods=["GET"])
@cross_origin(supports_credentials=True)
@AppConfig.require_appkey
def get_property_image_from_id():

    image_id = request.args.get("image_id")
    img_index = int(request.args.get("img_index"))

    if image_cache.contains(image_id):  # check cache
        img_slice = image_cache.get(image_id)[img_index]
    else:  # make expensive db call
        image_cache.store_image(image_id)
        img_slice = image_cache.get_image_slice(image_id, img_index)

    response = app.response_class(
        response=img_slice,
        status=200,
        mimetype="application/json",
    )

    return response


@app.route("/api/enumerations", methods=["GET"])
@cross_origin(supports_credentials=True)
@AppConfig.require_appkey
def get_enumerations():

    data = EnumerationsController.get_all()
    response = app.response_class(
        response=json.dumps(data), status=200, mimetype="application/json"
    )
    return response


@app.route("/api/get_cities_and_sample_addresses", methods=["GET"])
@cross_origin(supports_credentials=True)
@AppConfig.require_appkey
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
        print("APP URL: https://localhost:5050\n")
        print(f"Production DB URI: {os.environ['DB_URI']}")
        serve(app, host="0.0.0.0", port=5050)  # run production server
    else:
        app.run(debug=True, port=5050)  # run default flask server
