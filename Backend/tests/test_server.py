import json 
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))

print("os.environ]")
print(os.environ["API_KEY"])
print(os.environ["API_KEY"])
print(os.environ["API_KEY"])
print(os.environ["API_KEY"])
print(os.environ["API_KEY"])
print(os.environ["API_KEY"])
''' REQUIREMENTS: have server running on localhost:5000 '''

def test_authenticated_request():

    res = requests.get(
        url=f"http://localhost:5000/?key={os.environ['API_KEY']}", 
    )
    assert res.status_code == 200

    print("Authenticated request test passed")


def test_unauthenticated_request():

    res = requests.get(
        url="http://localhost:5000" 
    )
    assert res.status_code == 401

    print("Unauthenticated request test passed")


def test_get_adjacent_nodes():
    res = requests.post(
        url=f"http://localhost:5000/api/adjacent_nodes?key={os.environ['API_KEY']}", 
        data=json.dumps({"lng" :  -79.205745, "lat" : 43.810167 })
        
    )
    print(res.text)
    assert res.status_code == 200
    print("Get adjacent nodes test passed")

def test_get_adjacent_nodes_heroku():
    res = requests.post(
        url=f"https://ai-backend-flask.herokuapp.com/api/adjacent_nodes?key={os.environ['API_KEY']}", 
        data=json.dumps({"lng" :  -79.205745, "lat" : 43.810167 })
        
    )
    print(res.text)
    assert res.status_code == 200
    print("Get adjacent nodes test passed")


def test_get_amenities_from_id():
    res = requests.get(
        url=f"http://localhost:5000/api/amenities?key={os.environ['API_KEY']}", 
        params={"id" : "00159f42-8e6d-4c85-ad17-28942a8dd700"}
    )
    print(res.text)
    assert res.status_code == 200
    print("Get adjacent nodes test passed")


def test_enumerations_get():

    res = requests.get(
        url=f"http://localhost:5000/api/enumerations?key={os.environ['API_KEY']}", 
    )
    print(res.text)
    assert res.status_code == 200


    print("Authenticated request test passed")


def test_authenticated_request_heroku():

    res = requests.get(
        url=f"https://ai-backend-flask.herokuapp.com/?key={os.environ['API_KEY']}", 
    )
    assert res.status_code == 200

    print("Authenticated request test passed")



def test_get_unauth_adjacent_nodes():
    res = requests.post(
        url="http://ai-backend-flask.herokuapp.com/api/adjacent_nodes?key=12312",
        data=json.dumps({"lng" :  -79.205745, "lat" : 43.810167 })
    )
    print(res.text)
    assert res.status_code == 401
    print("Get adjacent nodes test passed")

# def test_get_unauth_adjacent_nodes():
#     res = requests.post(
#         url="http://localhost:5000/api/adjacent_nodes?key=12312",
#         data=json.dumps({"lng" :  -79.205745, "lat" : 43.810167 })
#     )
#     print(res.text)
#     assert res.status_code == 200
#     print("Get adjacent nodes test passed")