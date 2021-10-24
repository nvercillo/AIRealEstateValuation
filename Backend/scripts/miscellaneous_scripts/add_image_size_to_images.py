""" 
Description: seed database with data currently cached in files and geoencode amenity information

"""
import sys

sys.path.insert(0, "..")  # import parent folder
import time
import os
import requests
import json
import urllib
import csv
from models import Image
from flask_sqlalchemy import SQLAlchemy
from server import db
from sqlalchemy.dialects.postgresql import insert
import urllib
import threading

image_model = Image()

images = image_model._query_all()

print(images)
