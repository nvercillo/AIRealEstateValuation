import sys
sys.path.insert(0,'..') # import parent folder 
from models import Property 
import random
from numpy import random
from scipy.spatial import distance
from constant_enums import Enumerations

class AIModelController:
    
    def __init__(self):
        pass

    
    def predict_price(
        self, 
        lng, 
        lat, 
        address, 
        bathrooms, 
        dens,
        square_footage, 
        property_style,
        property_type,
        parking_spots,
        community,
        district
    ):
        
        return str(random.randint(700000, 1500000))