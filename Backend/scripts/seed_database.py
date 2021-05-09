import sys
sys.path.insert(0,'..') # import parent folder 
import os
import requests
import json
import urllib
import csv
from models import Property
from flask_sqlalchemy import SQLAlchemy
from server import db
from sqlalchemy.dialects.postgresql import insert
import urllib
import threading


google_api_base_url = "https://maps.googleapis.com/maps/api/geocode/json?"



class SeedDatabase:
    def get_google_maps(self, url):
        res = requests.get(url)
                                
        data = json.loads(res.content)
        coords = data.get("results")[0].get("geometry").get("location")
        
        return coords
        


    def seed_db_and_geoencode_amenities(self):

        with open('../../Data/data.csv') as f:
        
            count =0 
            to_insert = []
            db_insert_thread_pool = [] 
            for row in csv.DictReader(f, skipinitialspace=True):
                # print(row)
                to_update = []
                for k in row:
                    if " address" in k:
                        lon = k.split(" address")[0] + " longitude"
                        lat = k.split(" address")[0] + " latitude"

                        parameters = {
                            "address": row[k] + " Toronto, Ontario, Canada",
                            "key": os.environ['GOOGLE_MAPS_API_KEY']
                        }


                        url = f"{google_api_base_url}{urllib.parse.urlencode(parameters)}"
                        
                        limit_of_retries = 5
                        while limit_of_retries > 0:
                            try:
                                coords = self.get_google_maps(url)
                                d ={
                                    lon : coords['lng'],
                                    lat : coords['lat']
                                }
                                to_update.append(d)
                                break
                            except:
                                pass
                            
                            limit_of_retries -= 1
                        assert limit_of_retries >0, f"Google api failed on {url} passed the acceptable number of times"
                        
                        # to_update.append(row[k].strip())
                    
                # print(to_update)
                for d in to_update:
                    # print(d)
                    row.update(d)                
                 
                prop = Property(
                    address=row['address'],
                    sold_price=int(row['sold_price'].replace(",", "" )),
                    soldOn=row['soldOn'],
                    soldDate=row['Sold Date'],
                    listedOn=row['List Date'],
                    style=row['Style'],
                    longitude=row['longitude'],
                    latitude=row['latitude'],
                    data=json.dumps(row)
                )

                to_insert.append(prop)

                if count ==10:
                    print("\n\n\nINSERTING ANOTHER 100 OBJECTS \n\n\n")
                    
                    thread = threading.Thread(target=prop._insert, args=(to_insert,))
                    db_insert_thread_pool.append(thread)

                    thread.start()
                    prop._insert(to_insert)
                    
                    
                    count = -1
                    to_insert.clear()
    
                count +=1
                for t in db_insert_thread_pool:
                    if not t.is_alive():
                        # get results from thread
                        t.handled = True
                    
                db_insert_thread_pool =  [t for t in db_insert_thread_pool if not t.handled]


            for t in db_insert_thread_pool:
                t.join()

SeedDatabase().seed_db_and_geoencode_amenities()
