import json 
import sys
sys.path.insert(0,'..') # import parent folder 
from models import Property 
from numpy import random
from scipy.spatial import distance
from utils import  Math
from operator import itemgetter


class PropertiesController:

    RADIUS_OF_VIEWABILITY = 0.8 # km 
    CLOSEST_VIEWABLE_DISTANCE_DIFF = 0.01 # km 

    def __init__(self):
        self.property = Property(start_engine=True)

    def _get_by_id(self, id):
        return self.property._query_by_id(id)
    
    def query_by_coords(self, lng, lat):

        lon_diff = Math().calc_max_lon_deviance(self.RADIUS_OF_VIEWABILITY)
        lat_diff = Math().calc_max_lat_deviance(self.RADIUS_OF_VIEWABILITY, lng)

        res = self.property._query_by_coord_range(
            lng_above=lng+lon_diff,
            lng_below=lng-lon_diff,
            lat_above=lat+lat_diff,
            lat_below=lat-lat_diff
        )

        return res

    def _get_adjacent_nodes(self, lng, lat):


        res = self.query_by_coords(lng, lat) 

        _map = {}
        coords =  []
        for p in res:
            row = p.__as_small_dict__()
            
            lnglat = (row['lng'], row['lat'])
            coords.append(lnglat)

            _map[lnglat] = row
    
        closest = self.get_closest_nodes( (lng, lat), coords)

        arr = []
        for r in closest: 
            arr.append(_map[r])


        five_ids = []
        for i in range(5):
            five_ids.append(arr[i]['id'])

        return arr, five_ids

    def _get_community_data_from_nearest(self, five_nearest_ids):

        res = self.property._query_by_ids(five_nearest_ids)


        communities = []
        districts = []
        for r in res:
            data = json.loads(r.data)
            communities.append(data['Community'])
            districts.append(data["Municipality District"])
        
        return Math().mode(communities), Math().mode(districts)

    ''' HELPER FUNCTIONS '''
    def get_closest_nodes(self, node, nodes):
        dists = [] 

        for n in nodes: 
            dists.append((Math().calc_dist_bw_coords(node, n),n))

        dists = sorted(dists, key=itemgetter(0))
        
        stop_ind =len(dists)
        for i in range(len(dists)):
            if dists[i][0] > 1:  # grab nodes within 1 km 
                stop_ind = i
                break 

        arr = []
        for i in range(stop_ind):
            arr.append(dists[i][1])
            
        
        arr = sorted(arr, key=lambda x: x[0])  # sort all nodes by long

        # dedensify node clusters
        self.filter_for_relevant_nodes(
            sorted_arr=arr,
            critical_distance=self.CLOSEST_VIEWABLE_DISTANCE_DIFF
        )
        
        return arr

    ''' FUNCTION:   dedensify node clusters so frontend only rendering nodes with a certain 
                    amount of space between them '''
    def filter_for_relevant_nodes(self, sorted_arr, critical_distance):
        
        in_group = set({}) # set indexes of nodes

        for i in range(len(sorted_arr)):
            e = sorted_arr[i] 
            if i in in_group: continue

            critical_lon =  Math().calc_max_lon_deviance(critical_distance)
            critical_lat =  Math().calc_max_lat_deviance(critical_distance, e[1])

            _i = i - 1
            while _i >=0 and sorted_arr[_i][0] >  (e[0] - critical_lon):
                
                if sorted_arr[_i][1] > e[1] -critical_lat or \
                    sorted_arr[_i][1] <  e[1] + critical_lat: 
                    in_group.add(_i)

                _i -=1

        for ind in reversed([g for g in in_group]):
            sorted_arr.pop(ind)

# res = PropertiesController()._get_adjacent_nodes(-79.205745, 43.810167)
# print(len(res[0]))