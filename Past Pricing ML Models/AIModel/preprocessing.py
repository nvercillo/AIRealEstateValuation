import json
import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
# import immpo
# import requests 
# import tensorflow as tf 
# import numpy as np





with open('employee_file2.csv', mode='w', newline='') as csv_file:

    file1 = open('../Data/data.txt', 'r') 
    Lines = file1.readlines() 

    data = {}
    data['sold_price'] =  []
    data['address'] =  []
    data['longitude'] = []
    data['latitude'] = []
    data['bedNum'] =  []
    data['bathNum'] =  [] 
    data['sqarefootage'] =  []
    data['type'] =  []
    data['style'] =  []

    # prob not using this
    # data['lotSize'] =  []
    
    # elementary schools
    data['firstEleDist'] = []
    data['firstEleRat'] = []
    data['secondEleDist'] = []
    data['secondEleRat'] = [] 
    data['thirdEleDist']= [] 
    data['thirdEleRat'] = []

    # secondary schools
    data['firstSecDist'] = []
    data['firstSecRat'] = []
    data['secondSecDist'] = []
    data['secondSecRat'] = []


    # const array
    amenities = [ "Groceries",
        "Liquor Store",
        "Restaurants",
        "Coffee",
        "Bank",
        "Gas Station",
        "Health & Fitness",
        "Park",
        "Library",
        "Medical Care",
        "Pharmacy",
        "Mall",
        "Movie Theatre" ]

    # fill amenities
    for amenity in amenities:
        for i in range(0,3):
            data[amenity + " Distance" + str(i+1)] = []
    
    
    for line in Lines: 
        # put this in a try catch for performance
        INVALID = False
        # convert each line of code to a json obj
        line = json.loads(line)
        
        # process sold price:
        s = line['sold_price']
        
        #replace commas in price
        s = s.replace(",", "")
        
        # cast price to int
        data['sold_price'].append(int(s))

        # add all of these to data, none of these need processing
        data['address'].append(line['address'])
        data['longitude'].append(line['longitude'])
        data['latitude'].append(line['latitude'])

        # # get longitude and lat from coordinates
        # coords = forward_geocode(line['address'])
        # print(coords)

        # if 'error' in coords:
        #     INVALID  = True
        #     # throw error
        #     continue
        # data['longitude'].append(coords['lon'])
        # data['latitude'].append(coords['lat'])

        data['bedNum'].append(line['bedNum'])
        data['bathNum'].append(line['bathNum'])
        data['type'].append(line['Type'])
        data['style'].append(line['Style'])
        
        
        # lot size, should don't think we should use this
        # data['lotSize'].append(line['Lot Size'])



        # # process bed nums
        # s = data['bedNum']
        # s.split('+')
        # if len(s) > 1:
        #     data['bedNum'] = s[0]
        #     data['denNum'] = s[1]
        # else:
        #     data['']

        # process square footage
        s = line['sqarefootage']
        if s != 'n/a':
            if  '-' in s: 
                first = ""
                last = ""
                bd = True   # before dash 
                for i in range(0, len(s)):
                    if s[i] == '-':
                        bd = False
                    if bd:
                        first += s[i]
                    else:
                        last += s[i]
                first = int(first)
                last = int(last)
                s = first + (last - first) /2
            else:
                s = int(s)
        else:
            INVALID = True
            # throw error

        line['sqarefootage'] = s
        data['sqarefootage'].append(s)

        if not line['Amenities']:
            INVALID = True
            # throw error

        switchD =  {0: 'firstEleDist', 1: 'secondEleDist', 
            2: 'thirdEleDist', 3: 'firstSecDist', 4: 'secondSecDist'} 

        switchR =  {0: 'firstEleRat', 1: 'secondEleRat', 
            2: 'thirdEleRat', 3: 'firstSecRat', 4: 'secondSecRat'} 

        for i in range(0,3):
            if line['Nearest Schools'][i]['type'] != "Elementary":            
                INVALID = True
                # throw error
            else:
                data[switchD[i]].append(line['Nearest Schools'][i]['distance'])
                data[switchR[i]].append(line['Nearest Schools'][i]['rating'])

                
        for i in range(2, 5):
            if line['Nearest Schools'][i]['type'] != "Secondary":
                INVALID = True
                # throw error
            else:
                data[switchD[i]].append(line['Nearest Schools'][i]['distance'])
                data[switchR[i]].append(line['Nearest Schools'][i]['rating'])



        for i in range(0,3):
            for amenity in amenities:
                data[amenity + " Distance" + str(i+1)].append(line['Amenities'][amenity][i])

        # stop after 10 iterations
        if len(data['address']) >= 10:
            # ik dillon doesn't read these comments
            break


    
    fieldnames = ['sold_price',
        'address'
        'longitude'
        'latitude',
        'bedNum'
        'bathNum'
        'sqarefootage',
        'type'
        'style'
        'longitude',

        # schools 
        'firstEleDist'
        'firstEleRat'
        'secondEleDist',
        'secondEleRat'
        'thirdEleDist'
        'thirdEleRat',
        'firstSecDist'
        'firstSecRat'
        'secondSecDist',
        'secondSecRat'
        
        # amenities 
        'Groceries Distance1'
        'Groceries Distance2'
        'Groceries Distance3'
        'Liquor Store Distance1',
        'Liquor Store Distance2',
        'Liquor Store Distance3',
        'Restaurants Distance1'
        'Restaurants Distance2'
        'Restaurants Distance3'
        'Coffee Distance1'
        'Coffee Distance2'
        'Coffee Distance3'
        'Bank Distance1',
        'Bank Distance2',
        'Bank Distance3',
        'Gas Station Distance1',
        'Gas Station Distance2',
        'Gas Station Distance3',
        'Health & Fitness Distance1',
        'Health & Fitness Distance2',
        'Health & Fitness Distance3',
        'Park Distance1',
        'Park Distance2',
        'Park Distance3',
        'Library Distance1',
        'Library Distance2',
        'Library Distance3',
        'Medical Care Distance1',
        'Medical Care Distance2',
        'Medical Care Distance3',
        'Pharmacy Distance1',
        'Pharmacy Distance2',
        'Pharmacy Distance3',
        'Mall Distance1',
        'Mall Distance2',
        'Mall Distance3',
        'Movie Theatre Distance1',
        'Movie Theatre Distance2',
        'Movie Theatre Distance3']

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    for row in data: 
        writer.writerow(row)
    
    

    # continue preprocessing
    


    print(data['firstEleDist'])



    

    # df = pd.DataFrame(data,columns=['sold_price', 'address', 
    #     'bedNum', 'bathNum','sqft', 
    #     'typeOfProperty', 'style', 'lotSize',
    #     'amenities', 'schools']) 



    # writer.writeheader()
    # writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
    # writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})



    # print(data[0].mean())







# # function used to get long and lat from address 
# def forward_geocode(address, city='Toronto', state = 'Ontario', country = 'Canada'):
#     # api key
#     apiKey = '3c9e96b06652f7'

#     # urlify address and add province, country
#     urledAddress = address.replace(' ', '%20') + '%20' + city + '%20' + state + '%20' + country

#     # request json continaing coordinates
#     url = 'https://us1.locationiq.com/v1/search.php?key=' + apiKey + '&q=' + urledAddress + 'newAd&format=json'
#     lon = -1
#     lat = -1
#     try:
#         response = requests.get(url)
#         data = response.json()[0]
#         lon = data['lon']
#         lat = data['lat']
        
#     except:
#         # indicates that an error in this api occured
#         return {'error' : 'API',
#                 'address' : address}
    
#     return {'lon': lon, 'lat': lat, 'address': address}


# print (forward_geocode("3 Baird Avenue"))
# print (forward_geocode("210 Oakridge Drive'"))
# print (forward_geocode("4 Strathearn Boulevard"))
# print (forward_geocode('#2009 - 3 Rowntree Road'))
