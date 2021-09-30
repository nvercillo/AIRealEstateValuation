""" 
Description: seed database with associated images

"""
from re import sub
import sys

sys.path.insert(0, "../../")  # import parent folder
import time
import os
import requests
import json
import urllib
import csv
from models import Image
import pathlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
import urllib
import threading


class SeedDBwImages:
    def seed_db_w_images(self):
        os.chdir("../../../Data/Images")

        def insert_images(directory):

            # for _dir in directory[1]:
            #     print(_dir)
            print(directory)

        thread_pool = []

        sub_dirs = [x for x in os.walk(".") if x[0] != "."]

        for _dir in sub_dirs:
            thread = threading.Thread(target=insert_images, args=(_dir,))

            thread_pool.append(thread)
            thread.start()
            break

        for thread in thread_pool:
            thread.join()


SeedDBwImages().seed_db_w_images()
