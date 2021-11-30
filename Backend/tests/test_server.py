import json
import pytest
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
from pprint import pprint

load_dotenv(join(dirname(__file__), "../.env"))

LOCAL_URL = "http://localhost:5050"
PROD_URL = os.environ["PRODUCTION_BACKEND_URI"]

""" REQUIREMENTS: have server running on localhost:5050 """
servers_to_test = [
    "localhost"
    # , "production"
]


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [False])
def test_home_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL

    try:
        if authenticated:
            # URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(url=URL, params={"key": os.environ["API_KEY"]})
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)
            assert res.status_code == 200

    except Exception as e:
        raise Exception(
            f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [True, False])
def test_amenities(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/amenities"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(
                url=URL, params={"id": "eec7984d-e86e-441e-a0b7-4474cb7ff97d"}
            )
            pprint(".")
            pprint(".")
            pprint(res.text)
            pprint(".")
            pprint(".")
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)

            assert res.status_code == 401

        pprint(
            f"PASSED test_amenities: environment {environment}, authenticated {authenticated}"
        )
    except Exception as e:
        raise Exception(
            f"TEST test_amenities FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [True, False])
def test_enumerations_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/enumerations"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(url=URL)
            pprint(".")
            pprint(".")
            pprint(res.text)
            pprint(".")
            pprint(".")
            assert res.status_code == 200
            data = json.loads(res.text)
            assert isinstance(data, dict)
            assert len(data) > 0
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

        pprint(
            f"PASSED test_home_endpoint: environment {environment}, authenticated {authenticated}"
        )
    except Exception as e:
        raise Exception(
            f"TEST test_home_endpoint FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [True, False])
def test_adjacent_nodes_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/adjacent_nodes"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            pprint(URL)
            res = requests.post(
                url=URL,
                data=json.dumps(
                    {
                        "lng": -79.205745,
                        "lat": 43.810167,
                        "Sqaurefootage": "900-999",
                        "Type": "Detached",
                        "Style": "Loft",
                        "Bedrooms": 2,
                        "Dens": 2,
                        "Bathrooms": 3,
                        "ParkingTotal": 4,
                    }
                ),
            )
            pprint(".")
            pprint(".")
            pprint(res.text)
            pprint(".")
            pprint(".")
            assert res.status_code == 200
            data = json.loads(res.text)

            print(f"PREDICTED PRICE =  {data['predicted_price']}")
            assert isinstance(data, dict)
        else:
            res = requests.post(
                url=URL, data=json.dumps({"lng": -79.205745, "lat": 43.810167})
            )
            assert res.status_code == 401

        print(
            f"PASSED test_home_endpoint: environment {environment}, authenticated {authenticated}"
        )
    except Exception as e:
        raise Exception(
            f"TEST test_home_endpoint FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [True, False])
def test_image_ids_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/property_images_ids"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(
                url=URL, params={"property_id": "0f71385b-64fe-425d-b9b8-aba3f751c7a9"}
            )
            pprint(res.text)
            res = requests.get(
                url=URL, params={"property_id": "--this-property-id-doesnt-exist "}
            )
            pprint(res.text)
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

    except Exception as e:
        raise Exception(
            f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize("environment", servers_to_test)
@pytest.mark.parametrize("authenticated", [True])
def test_image_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/property_images"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            # res = requests.get(
            #     url=URL,
            #     params={
            #         "image_id": "---invalid---",
            #         "img_index": 0,
            #     },
            # )
            # assert res.status_code == 200
            # print(res.text)
            res = requests.get(
                url=URL,
                params={
                    "image_id": "02a17044-b120-4723-88d8-d98b41908dcc",
                    "img_index": 0,
                },
            )
            print(res.text)
            assert res.status_code == 200
            # res = requests.get(
            #     url=URL,
            #     params={
            #         "image_id": "0018a5b3-232c-43e3-9b9d-7d8bba264ffc",
            #         "img_index": 0,
            #     },
            # )
            # # assert res.status_code == 200
            # print(res.text)
            # res = requests.get(
            #     url=URL,
            #     params={
            #         "image_id": "001072f9-d6e6-4aa7-8e82-42f58627555c",
            #         "img_index": 0,
            #     },
            # )
            # assert res.status_code == 200
            # print(res.text)
            # res = requests.get(
            #     url=URL,
            #     params={
            #         "image_id": "001b30b9-fcd0-47bd-a495-af5c4327fee9",
            #         "img_index": 0,
            #     },
            # )
            # assert res.status_code == 200
            # print(res.text)
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

    except Exception as e:
        raise Exception(
            f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )
