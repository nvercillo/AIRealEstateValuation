"""
Description: read photo information files describing the link and id of properties in database. Link these properties with the respective images

"""

import sys

sys.path.insert(0, "../../")  # import parent folder
import os
import requests
import json
import uuid
import urllib
import csv
import pathlib
from models import Property
from utils import AlchemyEncoder
from flask_sqlalchemy import SQLAlchemy
import threading
from PIL import Image
from uuid import UUID


print("Querying all properties ... ")

os.chdir("../../../Data/Images")
property_model = Property()
properties = property_model._query_all()

print("GOT ALL DATA")


def dump_images(page_start, page_end, thread_num):
    arr = []
    for i in range(page_start, page_end):

        prop = properties[i]

        json_obj = json.loads(prop.data)

        link = json_obj["weblink"]

        data = {"id": prop.id, "address": prop.address, "link": str(link)}

        data["id"] = str(data["id"])

        arr.append(data)

    parent_dir = str(pathlib.Path(__file__).parent.resolve())
    file_suffix = f"/photo_info_{thread_num}"

    dir_path = parent_dir + file_suffix
    os.mkdir(dir_path)

    f = open(f"{dir_path}/{file_suffix}.json", "w+")
    f.write(json.dumps(arr))


N = 25  # number of image ripping threads

thread_pool = []
incr = len(properties) // N

start = 1
end = incr
for i in range(N):

    thread = threading.Thread(target=dump_images, args=(start, end, i + 1))
    thread_pool.append(thread)

    thread.start()

    start = end + 1
    end += incr

for thread in thread_pool:
    thread.join()


# page_nums = { int(_dir.split("page_num_")[1]) : (_dir, {})   for _dir in  os.listdir() if _dir != "page_ranges.txt"}

# f = open("page_ranges.txt", "r")
# num_pages = int(f.read())

# parent = os.getcwd()
# for i in page_nums:
#     os.chdir(page_nums[i][0])  # gets the directory path
#     sub_parent = os.getcwd()

#     iterations = os.listdir()

#     for iteration in iterations:
#         os.chdir(iteration)

#         image_links = os.listdir()
#         page_nums[i][1][iteration] = image_links

#         os.chdir(sub_parent)

#     os.chdir(parent)


# def dump_images(page_start, page_end):
#     parent = os.getcwd()
#     address_queue = []
#     for i in range(page_start, page_end+1):
#         if i in page_nums:


#             all_photo_info = []
#             for iteration in page_nums[i][1]:

#                 iteration_num = int(iteration.split("iteration_")[1])


#                 info_uri = f"{parent}/{page_nums[i][0]}/{iteration}/photos_info.json"

#                 f = open(info_uri, "r")

#                 photo_info = json.loads(f.read())


#                 if len(photo_info) ==0:
#                     continue

#                 address = photo_info[0]['address']
#                 address = "508 - 1 Rean Drive S"


#                 def parse_address(address):

#                     dig_inds = []

#                     for j in range(len(address)):
#                         if address[j].isnumeric():
#                             dig_inds.append(j)

#                     started_num1= False
#                     started_num2= False

#                     for j in range(1, len(dig_inds)):
#                         if dig_inds[j] - dig_inds[j-1] == 4 and address[dig_inds[j-1] +2] == "-":
#                             for k in range(j+1, len(dig_inds)):
#                                 if dig_inds[k] != dig_inds[k-1] +1:
#                                     return address[k: ], True

#                             try:
#                                 return address[  dig_inds[len(dig_inds) -1] +2 : ] , True
#                             except:
#                                 return address, False

#                     return address, False


#                 address, shortened = parse_address(address)

#                 if not shortened:
#                     properties = property_model.session.query(Property).filter(
#                         Property.address == address
#                     ).all()


#                 else:
#                     properties = property_model.session.query(Property).filter(
#                         Property.address.like("%"+ address)
#                     ).all()


#                 # properties = property_model.session.query(Property).filter(
#                 #         Property.address.like()
#                 # ).all()


#                 # if len(all_photo_info) == 10:


#                 #     to_del = []
#                 #     i = len(all_photo_info) -1
#                 #     while i >=0:
#                 #         if len(all_photo_info[i]) ==0:
#                 #             to_del.append(i)
#                 #         i-=1


#                 #     for i in to_del:
#                 #         all_photo_info.pop(i)


#                 #     sorted(all_photo_info, key = lambda a : a[0]["address"])
#                 #     addresses = [ d[0]['address'] for d in all_photo_info if len(d) != 0]


#                 #     print(addresses)
#                 #     properties = property_model.session.query(Property).filter(
#                 #             Property.address.in_(addresses)
#                 #     ).all()

#                 #     print("GOT PROPERTIES ", properties)

#                 #     all_photo_info.clear()
#                 #     exit()


#                 # for photo in photos_info:


#                 # for photo_uri in page_nums[i][1][iteration]:

#                     # uri = f"{parent}/{page_nums[i][0]}/{iteration}/{photo_uri}"
#                     # f = open(uri, "r")
#                     # photos_txt_cnt = f.read()

#                     # print(photos_txt_cnt)

#                     # print(json.loads(photos_txt_cnt))

#                     # img_split_arr = img_link.split("_photo_num_")
#                     # photo_num = int(img_split_arr[1].split(".png")[0])
#                     # address = img_split_arr[0].replace("_", " ")

#                     # address_queue.append(address)
#                     # if len(address_queue) == 100:


#                     #     properties = property_model._query_all()

#                     #     print(properties)
#                     #     print(address_queue)


#                 #         address_queue.clear()


# dump_images(45, 46)


# # N = 25 # number of image ripping threads


# # thread_pool = []
# # incr = num_pages // N

# # start = 1
# # end = incr
# # for i in range(N):

# #     thread = threading.Thread(target=dump_images, args=(start,end))
# #     thread_pool.append(thread)

# #     thread.start()

# #     start = end+1
# #     end += incr

# #     break


# # for thread in thread_pool:
# #     thread.join()
# # res = Images()._query_all()
