import json 
import pytest
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))

LOCAL_URL = "http://localhost:5000"
PROD_URL = "https://ai-backend-flask.herokuapp.com"

''' REQUIREMENTS: have server running on localhost:5000 '''
@pytest.mark.parametrize("environment, authenticated", [
    ("localhost", True),
    ("localhost", False),
    ("production", True),
    ("production", False)
])
def test_home_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/"

    try: 
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(url=URL)
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401 

    except Exception as e:
        raise Exception(f"FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}")


@pytest.mark.parametrize("environment, authenticated", [
    ("localhost", True),
    ("localhost", False),
    ("production", True),
    ("production", False)
])
def test_amenities(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/amenities"

    try: 
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(
                url=URL,
                params={"id" : "00159f42-8e6d-4c85-ad17-28942a8dd700"}
            )
            print(".")
            print(".")
            print(res.text)
            print(".")
            print(".")
            assert res.status_code == 200
        else:
            res = requests.get(url=URL)

            assert res.status_code == 401

        print(f"PASSED test_amenities: environment {environment}, authenticated {authenticated}")
    except Exception as e:
        raise Exception(f"TEST test_amenities FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}")



@pytest.mark.parametrize("environment, authenticated", [
    ("localhost", True),
    ("localhost", False),
    ("production", True),
    ("production", False)
])
def test_enumerations_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/enumerations"

    try: 
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            res = requests.get(url=URL)
            print(".")
            print(".")
            print(res.text)
            print(".")
            print(".")
            assert res.status_code == 200
            data = json.loads(res.text)
            assert isinstance(data, dict)
            assert len(data) > 0
        else:
            res = requests.get(url=URL)
            assert res.status_code == 401

        print(f"PASSED test_home_endpoint: environment {environment}, authenticated {authenticated}")
    except Exception as e:
        raise Exception(f"TEST test_home_endpoint FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}")


@pytest.mark.parametrize("environment, authenticated", [
    ("localhost", True),
    # ("localhost", False),
    # ("production", True)
    # ("production", False)
])
def test_adjacent_nodes_endpoint(environment, authenticated):

    URL = LOCAL_URL if environment == "localhost" else PROD_URL
    URL += "/api/adjacent_nodes"

    try: 
        if authenticated:
            URL += f"?key={os.environ['API_KEY']}"
            print(URL)
            res = requests.post(
                url=URL, 
                data=json.dumps(
                    {
                        "lng" :  -79.205745, 
                        "lat" : 43.810167,
                        "Sqaurefootage" : "900-999" ,
                        "Type" : "Detached",
                        "Style" : "Loft",
                        "Bedrooms" : 2,
                        "Dens" : 2,
                        "Bathrooms" : 3,
                        "ParkingTotal" :  4
                    }
                )
                
            )
            print(".")
            print(".")
            print(res.text)
            print(".")
            print(".")
            assert res.status_code == 200
            data = json.loads(res.text)

            print(f"PREDICTED PRICE =  {data['predicted_price']}")
            assert isinstance(data, dict)
        else:
            res = requests.post(
                url=URL,
                data=json.dumps({"lng" :  -79.205745, "lat" : 43.810167 })
            )
            assert res.status_code == 401

        print(f"PASSED test_home_endpoint: environment {environment}, authenticated {authenticated}")
    except Exception as e:
        raise Exception(f"TEST test_home_endpoint FAILED RUN: environment {environment}, authenticated {authenticated}, exception: {e}")

