import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

res = requests.get(f"https://ai-backend-flask.herokuapp.com/api/enumerations?key={os.environ['API_KEY']}")

if res.status_code != 200:
    print("RUN FAILED")
    f = open("logfile.txt", "a+")
    f.write(f"Time failed: {current_time}")
    f.close()
else:
    print("RUN PASSED")