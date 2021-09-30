"""
Description: scrape images from a list of urls

"""

import sys
import os

sys.path.insert(0, "../../")
import threading
from Naked.toolshed.shell import execute_js, muterun_js
import json


parent = os.getcwd()
puppeteer_scaping_file_path = f"{parent}/puppeteer_scraping/scrape_images.js"

os.chdir("../../../Data/Images")

photo_info_path_arr = [_dir for _dir in os.listdir()]


def scrape_images(photo_info_path):
    print(f"Running script for thread {threading.get_ident()}")

    success = execute_js(f"{puppeteer_scaping_file_path} {photo_info_path}")

    print(
        f"Thread {threading.get_ident()} executed successfully"
        if success
        else f"Thread {threading.get_ident()} failed: {success}"
    )


parent = os.getcwd()
thread_pool = []

for photo_info_path in photo_info_path_arr:

    thread = threading.Thread(
        target=scrape_images, args=(parent + "/" + photo_info_path,)
    )
    thread_pool.append(thread)
    thread.start()

for thread in thread_pool:
    thread.join()
