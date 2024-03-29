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
from utils.utility_functions import safeprint

os.chdir("../../../Data/Images")


class SeedDBwImages:

    photo_paths_map = {}
    thread_work_nums_set = set({})

    thread_work_num_mutex = Lock()
    thread_work_num = 0

    def prepare_image_link_data(self):

        prefix = "./photo_info_"
        for _dir in os.walk("."):
            if isinstance(_dir, tuple):
                # print(_dir)
                rel_path = _dir[0]

                if len(rel_path) > 2 * len(prefix):
                    property_id = rel_path.split("/")[2]
                    pngs = _dir[2]

                    thread_work_num = int(rel_path.split(prefix)[1].split("/")[0])
                    self.thread_work_nums_set.add(thread_work_num)
                    if thread_work_num not in self.photo_paths_map:

                        self.photo_paths_map[thread_work_num] = {property_id: pngs}
                    else:
                        self.photo_paths_map[thread_work_num][property_id] = pngs

    def insert_worker(self):
        self.thread_work_num_mutex.acquire()
        self.thread_work_num += 1
        thread_work_num = self.thread_work_num
        self.thread_work_num_mutex.release()

        blob_arr = []
        image_arr = []
        for prop_id in (
            self.photo_paths_map[thread_work_num]
            if thread_work_num in self.photo_paths_map
            else []
        ):

            for prop_id in self.photo_paths_map[thread_work_num]:

                for png in self.photo_paths_map[thread_work_num][prop_id]:
                    image_id = png.split(".png")[0]
                    abs_file_name = (
                        f"photo_info_{thread_work_num}/{prop_id}/{image_id}.png"
                    )

                    with open(abs_file_name, "rb") as f:

                        image_binary = f.read()
                        imageslices = split_str_into_n_sized_parts(image_binary, 64000)

                        try:
                            # image_arr.append(
                            #     Image(
                            #         id=image_id,
                            #         property_id=prop_id,
                            #         num_blobs=len(imageslices),
                            #         skip_creation=False,
                            #     )
                            # )

                            for index, slice in enumerate(imageslices):
                                blob_arr.append(
                                    ImageBlob(
                                        blob_index=index,
                                        image_id=image_id,
                                        raw_image_binary=slice,
                                        skip_creation=False,
                                    )
                                )

                        except Exception as err:
                            print(err)

                    # if len(blob_arr) >= 50:
                    #     safeprint(
                    #         f"Inserting {len(image_arr)} images and {len(blob_arr)} blob"
                    #     )

                    #     try:
                    #         # Image(skip_creation=True)._insert(image_arr)
                    #         ImageBlob(skip_creation=True)._insert(blob_arr)
                    #     except Exception as err:
                    #         safeprint(err)

                    #     image_arr.clear()
                    #     blob_arr.clear()

    def seed_db_w_images(self):

        self.prepare_image_link_data()

        thread_pool = []
        for _ in self.thread_work_nums_set:

            thread = Thread(target=self.insert_worker, args=())
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()


SeedDBwImages().seed_db_w_images()


# (
#     "./photo_info_7/41b2622b-2e71-456b-b4c8-26b55aa6e1ff",
#     [],
#     [
#         "26445c00-cad3-43b4-8323-7e258a9f19a1.png",
#         "2b8ae14c-8ac3-4ee3-a6ed-d761a4c93687.png",
#         "716c0b5f-2829-4a70-ac3e-9772aa4cf42c.png",
#         "df1a08ea-f70a-4ec6-96f9-f833c1912d32.png",
#         "470a95f7-d4f4-422f-af2b-2b40c65de1ac.png",
#         "491a2c76-6e89-469e-949b-813e3b2f7f5b.png",
#         "7d671d4e-e695-4b70-b412-73307bdfaad0.png",
#         "0cd36c67-1564-4be5-95fa-e34663fd6953.png",
#         "fdc93312-4500-4220-be2d-4b1812ad51f5.png",
#         "506198d1-28c5-41c5-b640-1962ad831a3b.png",
#     ],
# )
