import sys
import random

sys.path.insert(0, "..")  # import parent folder
from models import Property
from numpy import random
from scipy.spatial import distance
from constants import Enumerations
import math


# from tensorflow import keras
# loaded_model = keras.models.load_model('ai-model')


class AIModelController:
    def __init__(self):
        pass

    def dummy_predict_price(self, *args):
        return format(random.randint(700000, 2000000), ",")

    # # Input columns titles
    # """[
    #     "squarefootage",
    #     "type",
    #     "style",
    #     "community",
    #     "municipality district",
    #     "bedrooms",
    #     "dens",
    #     "bathrooms",
    #     "parking total"
    # ]"""

    # # Example input
    # example_input = [
    #     "900-999",
    #     "Condo Apartment",
    #     "Apartment",
    #     "Black Creek",
    #     "W05",
    #     2,
    #     0,
    #     1,
    #     1
    # ]
    def predict_price(self, input_arr):
        # One-hot-encode arrays
        type_encode = "{'Condo Apartment':0, 'Co-op / Co-Ownership Apartment':1, 'Condo Townhouse':2, 'Townhouse':3, 'Detached':4, 'Semi-Detached':5}"
        style_encode = "{'Apartment':6, '2-Storey':7, 'Bachelor/Studio':8, 'Stacked Townhouse':9, '3-Storey':10, 'Loft':11, 'Bungalow':12}"
        district_encode_bin = "{'C12' : 'district_bin_0',\
                                'C04' : 'district_bin_1',\
                                'C09' : 'district_bin_2',\
                                'C03' : 'district_bin_3',\
                                'E02' : 'district_bin_4',\
                                'C02' : 'district_bin_4',\
                                'W07' : 'district_bin_5',\
                                'W02' : 'district_bin_6',\
                                'E01' : 'district_bin_6',\
                                'W01' : 'district_bin_6',\
                                'C13' : 'district_bin_7',\
                                'E03' : 'district_bin_7',\
                                'C06' : 'district_bin_7',\
                                'C07' : 'district_bin_8',\
                                'E06' : 'district_bin_8',\
                                'W03' : 'district_bin_8',\
                                'C14' : 'district_bin_8',\
                                'W08' : 'district_bin_8',\
                                'C11' : 'district_bin_9',\
                                'E10' : 'district_bin_9',\
                                'C10' : 'district_bin_9',\
                                'E08' : 'district_bin_10',\
                                'W06' : 'district_bin_10',\
                                'C01' : 'district_bin_10',\
                                'C08' : 'district_bin_11',\
                                'W09' : 'district_bin_11',\
                                'W04' : 'district_bin_11',\
                                'E07' : 'district_bin_12',\
                                'W05' : 'district_bin_12',\
                                'E04' : 'district_bin_12',\
                                'C15' : 'district_bin_12',\
                                'E05' : 'district_bin_12',\
                                'E11' : 'district_bin_13',\
                                'E09' : 'district_bin_13',\
                                'W10' : 'district_bin_14'}"

        district_encode_int = "{'district_bin_12':17,\
                                'district_bin_9':18,\
                                'district_bin_10':19,\
                                'district_bin_3':20,\
                                'district_bin_11':21,\
                                'district_bin_13':22,\
                                'district_bin_14':23,\
                                'district_bin_7':24,\
                                'district_bin_1':25,\
                                'district_bin_8':26,\
                                'district_bin_4':27,\
                                'district_bin_6':28,\
                                'district_bin_5':29,\
                                'district_bin_2':30,\
                                'district_bin_0':31}"

        community_encode_bin = " {'Bridle Path-Sunnybrook-York Mills' : 'community_bin_0',\
                                'Lawrence Park South' : 'community_bin_1',\
                                'Lawrence Park North' : 'community_bin_2',\
                                'Forest Hill South' : 'community_bin_2',\
                                'Princess-Rosethorn' : 'community_bin_3',\
                                'Playter Estates-Danforth' : 'community_bin_3',\
                                'Forest Hill North' : 'community_bin_3',\
                                'Wychwood' : 'community_bin_3',\
                                'Bedford Park-Nortown' : 'community_bin_4',\
                                'Rosedale-Moore Park' : 'community_bin_4',\
                                'Kingsway South' : 'community_bin_4',\
                                'St. Andrew-Windfields' : 'community_bin_5',\
                                'Leaside' : 'community_bin_5',\
                                'Lambton Baby Point' : 'community_bin_6',\
                                'North Riverdale' : 'community_bin_6',\
                                'Casa Loma' : 'community_bin_6',\
                                'The Beaches' : 'community_bin_6',\
                                'Danforth' : 'community_bin_7',\
                                'East York' : 'community_bin_7',\
                                'Runnymede-Bloor West Village' : 'community_bin_7',\
                                'Trinity-Bellwoods' : 'community_bin_7',\
                                'Yonge-St. Clair' : 'community_bin_7',\
                                'Highland Creek' : 'community_bin_8',\
                                'Yonge-Eglinton' : 'community_bin_8',\
                                'Bayview Woods-Steeles' : 'community_bin_8',\
                                'Palmerston-Little Italy' : 'community_bin_8',\
                                'Danforth Village-East York' : 'community_bin_9',\
                                'Alderwood' : 'community_bin_9',\
                                'Stonegate-Queensway' : 'community_bin_9',\
                                'Roncesvalles' : 'community_bin_9',\
                                'Corso Italia-Davenport' : 'community_bin_9',\
                                'Edenbridge-Humber Valley' : 'community_bin_10',\
                                'Annex' : 'community_bin_10',\
                                'Humewood-Cedarvale' : 'community_bin_10',\
                                'Newtonbrook East' : 'community_bin_10',\
                                'Maple Leaf' : 'community_bin_10',\
                                'Woodbine Corridor' : 'community_bin_11',\
                                'Mount Pleasant East' : 'community_bin_11',\
                                'Greenwood-Coxwell' : 'community_bin_11',\
                                'Woodbine-Lumsden' : 'community_bin_11',\
                                'Humberlea-Pelmo Park W4' : 'community_bin_11',\
                                'OConnor-Parkview' : 'community_bin_11',\
                                'Cliffcrest' : 'community_bin_11',\
                                'Oakwood-Vaughan' : 'community_bin_11',\
                                'Cabbagetown-South St. James Town' : 'community_bin_12',\
                                'Banbury-Don Mills' : 'community_bin_12',\
                                'Lansing-Westgate' : 'community_bin_12',\
                                'Caledonia-Fairbank' : 'community_bin_12',\
                                'East End-Danforth' : 'community_bin_12',\
                                'Bathurst Manor' : 'community_bin_12',\
                                'Blake-Jones' : 'community_bin_12',\
                                'Beechborough-Greenbrook' : 'community_bin_12',\
                                'New Toronto' : 'community_bin_12',\
                                'University' : 'community_bin_13',\
                                'Dufferin Grove' : 'community_bin_13',\
                                'Junction Area' : 'community_bin_13',\
                                'South Riverdale' : 'community_bin_13',\
                                'Willowdale West' : 'community_bin_13',\
                                'Scarborough Village' : 'community_bin_13',\
                                'Willowridge-Martingrove-Richview' : 'community_bin_13',\
                                'Centennial Scarborough' : 'community_bin_13',\
                                'High Park-Swansea' : 'community_bin_13',\
                                'Thistletown-Beaumonde Heights' : 'community_bin_13',\
                                'Dovercourt-Wallace Emerson-Junction' : 'community_bin_14',\
                                'Englemount-Lawrence' : 'community_bin_14',\
                                'High Park North' : 'community_bin_14',\
                                'South Parkdale' : 'community_bin_14',\
                                'Birchcliffe-Cliffside' : 'community_bin_14',\
                                'Oakridge' : 'community_bin_14',\
                                'Clanton Park' : 'community_bin_14',\
                                'Hillcrest Village' : 'community_bin_14',\
                                'Rexdale-Kipling' : 'community_bin_14',\
                                'Rouge E10' : 'community_bin_14',\
                                'Broadview North' : 'community_bin_14',\
                                'Newtonbrook West' : 'community_bin_14',\
                                'Weston-Pellam Park' : 'community_bin_14',\
                                'Rouge E11' : 'community_bin_15',\
                                'Willowdale East' : 'community_bin_15',\
                                'Long Branch' : 'community_bin_15',\
                                'Humber Heights' : 'community_bin_15',\
                                'Humber Summit' : 'community_bin_15',\
                                'Parkwoods-Donalda' : 'community_bin_15',\
                                'Humberlea-Pelmo Park W5' : 'community_bin_15',\
                                'Wexford-Maryvale' : 'community_bin_15',\
                                'Rustic' : 'community_bin_15',\
                                'Waterfront Communities C8' : 'community_bin_16',\
                                'Steeles' : 'community_bin_16',\
                                'Markland Wood' : 'community_bin_16',\
                                'Milliken' : 'community_bin_16',\
                                'North St. James Town' : 'community_bin_16',\
                                'Islington-City Centre West' : 'community_bin_16',\
                                'Don Valley Village' : 'community_bin_16',\
                                'Eringate-Centennial-West Deane' : 'community_bin_16',\
                                'Kensington-Chinatown' : 'community_bin_16',\
                                'Bay Street Corridor' : 'community_bin_16',\
                                'Clairlea-Birchmount' : 'community_bin_16',\
                                'Rockcliffe-Smythe' : 'community_bin_17',\
                                'Tam OShanter-Sullivan' : 'community_bin_17',\
                                'Waterfront Communities C1' : 'community_bin_17',\
                                'Brookhaven-Amesbury' : 'community_bin_17',\
                                'Downsview-Roding-CFB' : 'community_bin_17',\
                                'Ionview' : 'community_bin_17',\
                                'Niagara' : 'community_bin_17',\
                                'Mount Pleasant West' : 'community_bin_17',\
                                'Mimico' : 'community_bin_17',\
                                'Agincourt North' : 'community_bin_17',\
                                'Victoria Village' : 'community_bin_17',\
                                'Guildwood' : 'community_bin_17',\
                                'Little Portugal' : 'community_bin_17',\
                                'Moss Park' : 'community_bin_17',\
                                'Briar Hill-Belgravia' : 'community_bin_18',\
                                'Church-Yonge Corridor' : 'community_bin_18',\
                                'West Hill' : 'community_bin_18',\
                                'York University Heights' : 'community_bin_18',\
                                'Regent Park' : 'community_bin_18',\
                                'Westminster-Branson' : 'community_bin_18',\
                                'Pleasant View' : 'community_bin_18',\
                                'Weston' : 'community_bin_18',\
                                'Etobicoke input_arrrk' : 'community_bin_20',\
                                'Eglinton East' : 'community_bin_21',\
                                'Flemingdon Park' : 'community_bin_21',\
                                'Woburn' : 'community_bin_21',\
                                'Malvern' : 'community_bin_21',\
                                'West Humber-Clairville' : 'community_bin_21',\
                                'Kingsview Village-The Westway' : 'community_bin_21',\
                                'Humbermede' : 'community_bin_21',\
                                'Keelesdale-Eglinton West' : 'community_bin_21',\
                                'Mount Dennis' : 'community_bin_21',\
                                'Glenfield-Jane Heights' : 'community_bin_21',\
                                'Mount Olive-Silverstone-Jamestown' : 'community_bin_22',\
                                'Crescent Town' : 'community_bin_22',\
                                'Elms-Old Rexdale' : 'community_bin_23',\
                                'Black Creek' : 'community_bin_23'}"

        community_encode_int = "{'community_bin_23':32,\
                                'community_bin_18':33,\
                                'community_bin_17':34,\
                                'community_bin_15':35,\
                                'community_bin_21':36,\
                                'community_bin_2':37,\
                                'community_bin_19':38,\
                                'community_bin_22':39,\
                                'community_bin_9':40,\
                                'community_bin_4':41,\
                                'community_bin_14':42,\
                                'community_bin_16':43,\
                                'community_bin_10':44,\
                                'community_bin_13':45,\
                                'community_bin_20':46,\
                                'community_bin_12':47,\
                                'community_bin_6':48,\
                                'community_bin_3':49,\
                                'community_bin_11':50,\
                                'community_bin_5':51,\
                                'community_bin_8':52,\
                                'community_bin_7':53,\
                                'community_bin_1':54,\
                                'community_bin_0':55}"

        # Create dictionaries with eval()
        Type_Dict = eval(type_encode)
        Style_Dict = eval(style_encode)
        Community_Dict_Bin = eval(community_encode_bin)
        Community_Dict_Int = eval(community_encode_int)
        District_Dict_Bin = eval(district_encode_bin)
        District_Dict_Int = eval(district_encode_int)

        # Normalization array
        normalize = [
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.25000000e-01,
            2.50000000e-01,
            1.42857143e-01,
            1.25000000e-01,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            1.00000000e00,
            3.33808201e-01,
        ]

        # Addition array
        addition = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            -0.14285714,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            -1.84310893,
        ]

        def process_array(input_array):

            output_array = [0] * 57

            # type and style
            output_array[Type_Dict[input_array[1]]] = 1
            output_array[Style_Dict[input_array[2]]] = 1

            # bedrooms - 13, dens - 14, bathrooms - 15, parking total - 16
            output_array[13] = input_array[5]
            output_array[14] = input_array[6]
            output_array[15] = input_array[7]
            output_array[16] = input_array[8]

            # municipality district and community
            output_array[Community_Dict_Int[Community_Dict_Bin[input_array[3]]]] = 1
            output_array[District_Dict_Int[District_Dict_Bin[input_array[4]]]] = 1

            # squarefootage
            output_array[56] = math.log(
                sum(list(map(int, input_array[0].split("-")))) / 2
            )

            # normalize and addition
            output_array = [
                num1 * num2 + num3
                for num1, num2, num3 in zip(output_array, normalize, addition)
            ]
            ml_array = [output_array]
            return ml_array

        # Testing
        output = process_array(input_arr)
        print(output)

        prediction = loaded_model.predict(output)
        y_0 = prediction[0][0]
        print("Prediction with scaling - {}", format(y_0))
        y_0 -= 0.029517638588912886
        y_0 /= 1.4398848092152627e-07
        y_0 = format(int(y_0 / 1000) * 1000, ",")

        print("Housing Price Prediction  - ${}".format(y_0))
        return y_0
