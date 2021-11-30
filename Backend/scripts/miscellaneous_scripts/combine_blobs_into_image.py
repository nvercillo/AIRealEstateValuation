""" 
Description: seed database with associated images

"""
import sys
from pprint import pprint
import base64

sys.path.insert(0, "../../")  # import parent folder
import os
from models.image_model import Image
from models.blob_model import ImageBlob
import pathlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
import urllib
from threading import Thread, Lock
from utils.utility_functions import split_str_into_n_sized_parts


imgs = ImageBlob(start_engine=True)._query_all(limit=100)


raw = b""
for img in imgs:
    raw += img.raw_image_binary


f = open("demofile3.jpg", "wb")
f.write(raw)
f.close()


# print(imgs)
