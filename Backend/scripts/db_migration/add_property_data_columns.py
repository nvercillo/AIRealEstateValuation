import json
import sys
from pprint import pprint

from sqlalchemy.orm import query

sys.path.insert(0, "../../")  # import parent folder
from controllers import properties_controller


def update_cols_with_json_data():
    PropertiesController = properties_controller.PropertiesController()

    with PropertiesController.property.engine.connect() as con:

        properties = PropertiesController.property._query_all()

        for p in properties:

            json_dict = json.loads(p.data)
            bed_str = json_dict["bedNum"]
            bed_str_arr = bed_str.split("+")
            num_beds = int(bed_str_arr[0]) if bed_str_arr[0] != "n/a" else 0
            num_dens = int(bed_str_arr[1]) if len(bed_str_arr) > 1 else 0
            square_footage = str(json_dict["sqarefootage"])
            prop_type = str(json_dict["Type"])
            parking_total = int(float(json_dict["Parking Total"]))
            num_bathrooms = (
                int(json_dict["bathNum"]) if json_dict["bathNum"] != "n/a" else 0
            )

            query_str = f'UPDATE AI_PROPERTY_DATA SET `num_bedrooms` = {num_beds} WHERE ID = "{p.id}";'
            print(query_str)
            con.execute(query_str)

            query_str = f'UPDATE AI_PROPERTY_DATA SET `num_bathrooms` = {num_bathrooms} WHERE ID = "{p.id}";'
            print(query_str)
            con.execute(query_str)

            if num_dens > 0:
                query_str = f'UPDATE AI_PROPERTY_DATA SET `num_dens` = {num_dens} WHERE ID = "{p.id}";'
                print(query_str)
                con.execute(query_str)

            query_str = f'UPDATE AI_PROPERTY_DATA SET `square_footage` = "{square_footage}" WHERE ID = "{p.id}";'
            print(query_str)
            con.execute(query_str)

            query_str = f'UPDATE AI_PROPERTY_DATA SET `property_type` = "{prop_type}" WHERE ID = "{p.id}";'
            print(query_str)
            con.execute(query_str)

            query_str = f'UPDATE AI_PROPERTY_DATA SET `parking_spots` = {parking_total} WHERE ID = "{p.id}";'
            print(query_str)
            con.execute(query_str)

    # pprint(properties)


update_cols_with_json_data()
