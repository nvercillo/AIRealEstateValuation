""" 
Description: seed database with associated images

"""
import sys
from pprint import pprint

sys.path.insert(0, "../../")  # import parent folder
import os
from models.image_model import Image
import pathlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
import urllib
from threading import Thread, Lock


os.chdir("../../../Data/Images")

Image._select_from_where(attributes="")


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
        thread_work_num = self.thread_work_num
        self.thread_work_num += 1
        self.thread_work_num_mutex.release()

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

                        image_arr.append(
                            Image(
                                id=image_id,
                                property_id=prop_id,
                                raw_image_binary=image_binary,
                            )
                        )
                    if len(image_arr) == 10:
                        print(f"Inserting max of {len(image_arr)} images")
                        try:
                            Image()._insert(image_arr)
                        except:
                            pass
                        image_arr.clear()

    def seed_db_w_images(self):

        self.prepare_image_link_data()

        thread_pool = []
        for _ in self.thread_work_nums_set:

            # self.insert_worker()

            thread = Thread(target=self.insert_worker, args=())
            thread_pool.append(thread)
            thread.start()

            # break
        for thread in thread_pool:
            thread.join()

        # print(self.photo_paths_map[1]["008add4a-afd5-42cf-8d0e-9acb5c94b40a"])


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
