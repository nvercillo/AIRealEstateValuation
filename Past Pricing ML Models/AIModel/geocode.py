import json
import requests
 
#forward geocoding function (address to coordinates)
def forward_geocode(address, city='Toronto', state = 'Ontario', country = 'Canada'):
    #api key
    apiKey = '3c9e96b06652f7'

    #urlify address and add province, country
    urledAddress = address.replace(' ', '%20') + '%20' + city + '%20' + state + '%20' + country

    #request json continaing coordinates
    url = 'https://us1.locationiq.com/v1/search.php?key=' + apiKey + '&q=' + urledAddress + 'newAd&format=json'
    data = None
    try:
        response = requests.get(url)
        data = response.json()[0]
    except:
        #return 0 as both coordinates indicating a failure to forward code the address
        return (0.0, 0.0)
    #print(data["lat"] + ' ,' + data["lon"])
    
    return (data["lat"], data["lon"])
    
  
