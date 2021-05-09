import sys
sys.path.insert(0,'..') # import parent folder 
import time 
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
    
    
    def seed_entire_db(self):
        log_mutex = threading.Lock()
        
        thread_pool = []
        for i in range(1 , 12 +1):
            thread = threading.Thread(
                target=self.seed_db_and_geoencode_amenities_for_csv_file,
                args=(i, log_mutex)
            )
        
            thread_pool.append(thread)
            thread.start()
            print(f"starting thread {i}")
            # break

        c =1
        for t in thread_pool:
 
            print(f'joining thread {c}')
            t.join()
            c +=1 
            # break

    def seed_db_and_geoencode_amenities_for_csv_file(self, csv_ind, log_mutex):

        with open(f'../../Data/data_{csv_ind}.csv') as f:

            count =0 
            to_insert = []
            db_insert_thread_pool = [] 
            for row in csv.DictReader(f, skipinitialspace=True):

                # geoencoding 
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
                        
                        limit_of_retries = 10
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

                            time.sleep(3)
                        # assert limit_of_retries >0, f"Google api failed on {url} passed the acceptable number of times"
                        
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

                if count ==1:
                    print("\n\n\nINSERTING ANOTHER 100 OBJECTS \n\n\n")
                    
                    log_mutex.acquire()
                    
                    try: 
                        thread = threading.Thread(target=prop._insert, args=(to_insert.copy(),))
                        db_insert_thread_pool.append(thread)

                        thread.start()
                        f = open("seeding_log.txt", "a+")
                        f.write(f"THREAD {csv_ind} writing property {prop}")
                        f.close()
                    except:
                        f = open("seeding_log.txt", "a+")
                        f.write(f"THREAD {csv_ind} FFFFFAILED nearby {prop}")
                        f.close()

                    finally:
                        log_mutex.release()    
                    
                        count = -1
                        to_insert.clear()
    
                count +=1
                # for t in db_insert_thread_pool:
                #     if not t.is_alive():
                #         # get results from thread
                #         t.handled = True
                    
                # db_insert_thread_pool =  [t for t in db_insert_thread_pool if not t.handled]


            for t in db_insert_thread_pool:
                t.join()

SeedDatabase().seed_entire_db()
