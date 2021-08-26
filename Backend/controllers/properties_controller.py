import json 
import sys
sys.path.insert(0,'..') # import parent folder 
from models import Property 
from numpy import random
from scipy.spatial import distance
from scipy.stats import zscore
from utils import  Math
from operator import itemgetter

# from dotenv import load_dotenv
# from os.path import join, dirname
# load_dotenv(join(dirname(__file__), '../.env'))


class PropertiesController:

    RADIUS_OF_VIEWABILITY = 0.8 # km 
    CLOSEST_VIEWABLE_DISTANCE_DIFF = 0.01 # km 
    SEARCHABLE_DISTANCE = 2 # how big should we make the initial query in km 
    NUM_NEARBY_CONSIDERED_FOR_AI = 50

    def __init__(self):
        self.property = Property(start_engine=True)

    def _get_by_id(self, id):
        return self.property._query_by_id(id)
    
    def query_by_coords_and_filter(
        self, 
        lng, 
        lat, 
        filters=False,
        SEARCHING_DISTANCE=None
    ):

        if SEARCHING_DISTANCE is None:
            SEARCHING_DISTANCE = self.RADIUS_OF_VIEWABILITY
        
        lon_diff = Math().calc_max_lon_deviance(SEARCHING_DISTANCE)
        lat_diff = Math().calc_max_lat_deviance(SEARCHING_DISTANCE, lng)

        res = self.property._query_by_coord_range_and_filter(
            lng_above=float(lng)+float(3*lon_diff),
            lng_below=float(lng)-float(3*lon_diff),
            lat_above=float(lat)+float(lat_diff),
            lat_below=float(lat)-float(lat_diff),
            filters=filters
        )

        return res

    
    def get_location_ai_data(self):  # multi thread this to make it faster 

        nearby = self.query_by_coords_and_filter(
            self.longitude
            self.latitude,
            filters={"style" : self.style}
            SEARCHING_DISTANCE=SEARCHABLE_DISTANCE
        )

        distances = [] 
        prices = []
        
        # get the NUM_NEARBY_CONSIDERED_FOR_AI nearest properties and average their fitted lines
        for i in range(len(nearby)):
            node = nearby[i]         
            distances[i] = Math().calc_dist_bw_coords( 
                (self.latitude, self.longitude),
                (node.latitude, node.longitude)
            )

            prices[i] = node.sold_price
        

        max_iterations = min(self.NUM_NEARBY_CONSIDERED_FOR_AI, len(prices))
        

        ''' create z score array of distances '''         
        z_dists = stats.zscore(  # multi 
            np.array(
                # there are less nodes in the array than NUM_NEARBY_CONSIDERED_FOR_AI
                distances[:max_iterations]
            )
        )

        # ''' create z score array of distances '''
        # z_prices = stats.zscore( # multi 
        #     np.array(
        #         # there are less nodes in the array than NUM_NEARBY_CONSIDERED_FOR_AI
        #         prices[:max_iterations]
        #     )
        # )

        # after 1 standard deviations the output becomse insignificant
        z_dists = [1 * abs(z) for z in z_dists]   # score is now a variance, not absolute z_score
        # z_prices = [1 * abs(z) for z in z_prices]  # score is now a variance, not absolute z_score


        inverse_distance_scores_sum = 0 
        inverse_price_scores_sum = 0 
        

        for i in range(max_iterations):

            # 1/(x +0.1) normalized function using with a max of 10 using z_score
            inverse_distance_scores_sum += 1 / (z_dists[i] + 0.1)
            # inverse_price_scores_sum += 1 / (z_prices[i] + 0.1 )
        

                    
        # variables for the equation a * x *x + b*x + c 
        a = 0
        b = 0 
        c = 1


        # get the NUM_NEARBY_CONSIDERED_FOR_AI nearest properties and average their fitted lines
        for i in range(max_iterations):
            node = nearby[i]
            lng = node.longitude
            lat = node.latitude

            a_val = node.ai_data["a"] 
            b_val = node.ai_data["b"]
            
            dist_function_val = 1 / (z_dists[i] + 0.1)
            a += a_val * ( dist_function_val / inverse_distance_scores_sum )
            b += b_val * ( dist_function_val / inverse_distance_scores_sum )


        # used to find max of slope for negative if valued function
        variances = []

        stop_ind = -1
        inverse_variance_sum = 0 
        for i in range(max_iterations):

            node = nearby[i]
            variances.append( a * distances[i] **2  + b * distances[i] + c )

            if i > 1 and a < 0 and variances[i] < variances[i-1] : # max reached
                stop_ind = i
                break
            else:
                
                # 1/(x +0.1) normalized function using with a max of 10 using z_score
                inverse_variance_sum += 1 / ( variances[i] + 0.1)

        predicted_price = 0 
        for i in range(stop_ind):
            node = nearby[i]
            price = node.sold_price

            variance_function_val = 1 / ( variances[i] + 0.1)

            predicted_price += price * (variance_function_val / inverse_variance_sum)

            # calculate root sum squared val 
            RSS_of_variance += ( variance[i] * (variance_function_val / inverse_variance_sum) ) ** 2


        RSS_of_variance **= 0.5  # sqaure root squared sums

        relative_error = RSS_of_variance / predicted_price


        return {
            "predicted_price" : predicted_price,
            "relative_error" : relative_error
        }    
        



    def _get_adjacent_nodes(self, lng, lat):

        res = self.query_by_coords_and_filter(lng, lat) 

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
            if dists[i][0] > self.SEARCHABLE_DISTANCE:  # grab nodes within 1 km 
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

# res = PropertiesController()._get_adjacent_nodes( lng= -79.384610 ,lat = 43.697070)
# print(len(res[0]))