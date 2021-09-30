# DEPRECATED ...

"""
Description: scrape images from a list of urls

"""

import sys
import os, os.path

sys.path.insert(0, "../../")
import threading
from Naked.toolshed.shell import execute_js, muterun_js


# success = execute_js('scraping_functions/scrape_images.js')
thread_pool = []


try:
    f = open("../../../Data/Images/page_ranges.txt", "r")
except:
    print("Running get_max_page_range.js script")

    success = execute_js(f"puppeteer_scraping/get_max_page_range.js")
    f = open("../../../Data/Images/page_ranges.txt", "r")


num_pages = int(f.read())

print(num_pages)


def scrape_images(page_start, page_end):
    print(f"Running script {page_start} {page_end}")
    success = execute_js(f"puppeteer_scraping/scrape_images.js {page_start} {page_end}")


N = 25  # number of image ripping threads


incr = num_pages // N

start = 1
end = incr
for i in range(N):

    thread = threading.Thread(target=scrape_images, args=(start, end))
    thread_pool.append(thread)

    thread.start()

    start = end + 1
    end += incr

    # break


for thread in thread_pool:
    thread.join()
