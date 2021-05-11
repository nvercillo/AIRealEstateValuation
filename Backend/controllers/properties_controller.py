import sys
sys.path.insert(0,'..') # import parent folder 
from models import Property 
from numpy import random
from scipy.spatial import distance





class PropertiesController:
    
    def __init__(self):
        pass

    def _get_by_id(self, id):
        return Property._query_by_id(id).__as_dict__()

    def _get_closest_nodes(self, node, nodes):
        arr = distance.cdist([node], nodes)

        d = {}
        for i in range(len(arr[0])):
            d[tuple(nodes[i])] = arr[0][i]
        
        d = dict(sorted(d.items(), key=lambda item: item[1]))
        
        res = []
        c =0 
        for k in d.keys():
            if c ==200:
                break
            res.append(k)
            c+= 1

        return res


    def _get_adjacent_nodes(self, lgn, lat):
        res = Property._query_by_coords(lgn, lat) 
    
        _map = {}
        coords =  []
        for p in res:
            row = p.__as_small_dict__()
            
            lgnlat = (row['lgn'], row['lat'])
            coords.append(lgnlat)

            _map[lgnlat] = row
    

        closest = self._get_closest_nodes( (lgn, lat), coords)

        arr = []
        for r in closest: 
            arr.append(_map[r])

        return arr