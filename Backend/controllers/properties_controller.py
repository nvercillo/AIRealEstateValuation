import json 
import sys
sys.path.insert(0,'..') # import parent folder 
from models import Property 
from numpy import random
from scipy.spatial import distance
from utils import mode 


class PropertiesController:
    
    def __init__(self):
        self.property = Property(start_engine=True)

    def _get_by_id(self, id):
        return self.property._query_by_id(id)

    def _get_closest_nodes(self, node, nodes,):
        arr = distance.cdist([node], nodes)

        d = {}
        for i in range(len(arr[0])):
            d[tuple(nodes[i])] = arr[0][i]
        
        d = dict(sorted(d.items(), key=lambda item: item[1]))
        
        res = []
        c =0 
        for k in d.keys():
            if d[k] > 0.1:
                break
            if c ==300:
                break
            res.append(k)
            c+= 1

        return res


    def _get_adjacent_nodes(self, lng, lat):

        res = self.property._query_by_coords(lng, lat) 
    
        _map = {}
        coords =  []
        for p in res:
            row = p.__as_small_dict__()
            
            lnglat = (row['lng'], row['lat'])
            coords.append(lnglat)

            _map[lnglat] = row
    

        closest = self._get_closest_nodes( (lng, lat), coords)

        arr = []
        for r in closest: 
            arr.append(_map[r])


        five_ids = []
        for i in range(5):
            five_ids.append(arr[i]['id'])

        return arr, five_ids

    def _get_community_data_from_nearest(self, five_nearest_ids):

        res = self.property._query_by_ids(five_nearest_ids)
        print(res)


        communities = []
        districts = []
        for r in res:
            data = json.loads(r.data)
            communities.append(data['Community'])
            districts.append(data["Municipality District"])
        
        return mode(communities), mode(districts)