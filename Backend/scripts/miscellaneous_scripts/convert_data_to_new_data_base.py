"""
Description: 

"""

import sys

sys.path.insert(0, "..")  # import parent folder
import time
from copy import deepcopy
import os
import requests
import json
import urllib
import csv
from models import Property
from flask_sqlalchemy import SQLAlchemy
from server import db
from sqlalchemy.dialects.postgresql import insert
import urllib
import threading
import os
import uuid
import psycopg2
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload, load_only
from sqlalchemy.dialects.postgresql import UUID

import mysql.connector


""" PURPOSE OF THIS FILE is to convert all of our data over to the Cloud Platform """

prop_model = Property(not_insertion=True)
properties = prop_model._query_all()

copy_properties = []
for p in properties:
    copy_properties.append(
        PropertyData(
            p.address,
            p.sold_price,
            p.soldOn,
            p.soldDate,
            p.listedOn,
            p.longitude,
            p.latitude,
            p.style,
            p.data,
        )
    )

bh_prop_model = PropertyData(not_insertion=True)
bh_prop_model._insert(copy_properties)
