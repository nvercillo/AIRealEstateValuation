#!/usr/bin/python
import os
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))


''' INSTANTIATE SERVER '''
if __name__ == '__main__':
    if os.environ['PRODUCTION'] and os.environ['PRODUCTION'] == "True":
        print(os.environ['DB_URI'])
        print("Started production server .... :)")
        serve(app, host="0.0.0.0", port=5000) # run production server
    else: 
        app.run(debug=True)   # run default flask server 

''' END START UP SERVER '''



