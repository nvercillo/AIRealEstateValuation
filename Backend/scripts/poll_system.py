import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), "../.env"))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

res = requests.get(
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

f = open("logfile.txt", "a+")
if res.status_code != 200:
    print("RUN FAILED")
    f.write(f"Time failed: {current_time}")
else:
    print("RUN PASSED")
    f = open("logfile.txt", "a+")
    f.write(f"Time passed: {current_time}\n")

f.close()
