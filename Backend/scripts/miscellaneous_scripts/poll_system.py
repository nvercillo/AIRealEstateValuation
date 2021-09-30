""" 
Description: purpose is to poll heroku frontend and backend servers (to be deprecated)

"""


import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), "../.env"))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

res1 = requests.get(
    f"https://ai-backend-flask.herokuapp.com/api/enumerations?key={os.environ['API_KEY']}"
)
res2 = requests.get(f"https://ai-real-estate-valuator.herokuapp.com/")
print(res1)
print(res2)
print(
    f"https://ai-backend-flask.herokuapp.com/api/enumerations?key={os.environ['API_KEY']}"
)

line_count = 0
try:
    f = open("logfile.txt", "r")

    for line in f:
        if line != "\n":
            line_count += 1
    if line_count > 10000:
        f.close()
        f = open("logfile.txt", "w+")
        f.write("NEW FILE\n")
        f.close()
except:
    pass

file = open("logfile.txt", "w+")
line_count = 0
for line in file:
    if line != "\n":
        line_count += 1
file.close()

if line_count < 10:
    f = open("logfile.txt", "a+")
else:
    f = open("logfile.txt", "w")


if res1.status_code != 200 or res2.status_code != 200:
    print("RUN FAILED")
    f.write(f"Time failed: {current_time}")
else:
    print("RUN PASSED")
    f.write(f"Time passed: {current_time}\n")

f.close()
