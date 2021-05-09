import sys
sys.path.insert(0,'..') # import parent folder 
from constant_enums import Enumerations

class EnumerationsController:

    @staticmethod
    def get_all():
        data = {}
        gen = (e for e in Enumerations if '_' not in e.name)
        for e in gen:
            data[e.name] = e.value

        return data
    
