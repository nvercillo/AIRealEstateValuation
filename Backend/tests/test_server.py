import json
import pytest
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
from pprint import pprint

load_dotenv(join(dirname(__file__), "../.env"))

LOCAL_URL = "http://localhost:5000"
PROD_URL = "https://ai-backend-flask.herokuapp.com"

""" REQUIREMENTS: have server running on localhost:5000 """


@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
@pytest.mark.parametrize("authenticated", [True, True])
def test_home_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL


    try:
        if authenticated:
            # URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(url=URL, params={"key": os.environ['API_KEY']})
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

    except Exception as e:
        raise Exception(
            f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )


@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
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


@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
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


@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
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


@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
@pytest.mark.parametrize("authenticated", [True])
def test_image_ids_endpoint(environment, authenticated):


    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/property_images_ids"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(
                url=URL, params={"property_id": "5f70921b-6b76-4f54-9664-43372e570a3b"}
            )
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

@pytest.mark.parametrize(
    "environment",
    [
        # "localhost", "production"
        "localhost"
    ],
)
@pytest.mark.parametrize("authenticated", [True])
def test_image_endpoint(environment, authenticated):


    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/property_images"

    try:
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(
                url=URL, params={"image_id": "---invalid---"}
            )
            res = requests.get(
                url=URL, params={"image_id": "02a17044-b120-4723-88d8-d98b41908dcc"}
            )
            assert res.status_code == 200
            print(res.text)
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

        
    except Exception as e:
        raise Exception(
            f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}"
        )
