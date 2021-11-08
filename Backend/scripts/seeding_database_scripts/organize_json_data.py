""" 
Description: seed database with associated images

"""

import json
from re import A
import sys
from pprint import pprint

from numpy import isin
from sqlalchemy import exc

sys.path.insert(0, "../../")
from models.property_model import Property

prop_model = Property()
# properties = prop_model._query_all()

invalid = [
    ("8730c34f-3652-4cae-b4a8-49d83e534e44",),
    ("a6d51cb5-6833-4d27-81e4-c9cf9e5c0f5e",),
    ("882fdde1-5274-4000-8da0-4800344b7178",),
    ("97142322-2459-4e65-a449-0209df763f2a",),
    ("2f3ba50f-171b-4f70-8d6b-53fbe9eeb2c7",),
    ("d0e96bf7-e26d-491a-a679-2ac4fc92ee1d",),
    ("0f579a94-ca5a-4a5a-b677-8167388b53aa",),
    ("2a8d7e25-b6bb-4917-a138-25947f93736a",),
    ("376aab5d-ab46-45d0-b521-504727d5c4db",),
    ("47aee7ee-d8b3-47ca-af67-e7ebe5e66545",),
    ("7840d81c-98b4-4cc8-8dec-48ff36ec4804",),
    ("9c0346a7-6ceb-429d-9002-c3439ccf26f2",),
    ("a284b21e-3ce4-4ffa-90f0-3e41d34e0918",),
    ("e689d525-c518-4739-a8b2-014e2c273856",),
    ("fcb08780-8e5d-41c6-a7e1-cea4efe6a2ef",),
    ("04494da1-fecf-40fd-8879-4e3146566704",),
    ("3431b635-65dc-4262-b86a-9331d9de9e27",),
    ("5bc2eb2e-23ba-472e-92e4-10805634608f",),
    ("6344fb05-b809-42b7-b51a-4d4daea67bcb",),
    ("805316a8-b744-4dde-8fa6-949cb69eb143",),
    ("8d985f68-d452-496d-a66c-7dc49a7bdb4b",),
    ("a72ef33e-8ecf-4a1e-b5fe-5f5d9b92f235",),
    ("cdfeb471-90e0-466c-bb99-90c21a19d8c6",),
    ("d14f3b5e-f46b-4b86-b475-c3d03d4bdbaf",),
]

invalid = [i[0] for i in invalid]


properties = prop_model._query_all()


def get_invalid_ids():
    ids = prop_model._query("SELECT `id` FROM AI_PROPERTY_DATA;")

    invalid = []
    for id in ids:

        try:
            prop_model._query_by_id(id[0])
        except:
            invalid.append(id)

    print(f"invalid:  {invalid}")


def fix_broken_props(properties):
    for p in properties:

        if isinstance(p.data, dict):
            continue

        val = str(p.data).replace("\\", "")

        jstring = val.replace('"', '\\"')
        prop_model._query(
            f'UPDATE AI_PROPERTY_DATA SET `data` = "{jstring}" WHERE ID = "{p.id}";',
            select=False,
        )


# fix_broken_props(invalid)
for p in properties:
    if isinstance(p.data, dict):
        continue

    dic = p.data

    keys = sorted([e for e in dic.keys()])

    data = {}
    data["weblink"] = dic["weblink"]
    i = 0
    while i < len(keys):
        k1 = keys[i]
        arr = k1.split("#")
        if len(arr) > 1:

            amenity = arr[0].strip()

            if amenity not in data:
                data[amenity] = []
                for i in range(3):
                    data[amenity].append({})

            num = arr[1][0]
            field = arr[1][2:]
            if isinstance(dic[k1], str):
                dic[k1] = dic[k1].replace('"', "'")

            data[amenity][int(num) - 1][field] = dic[k1]

        i += 1

    jstring = json.dumps(data).replace('"', '\\"')
    prop_model._query(
        f'UPDATE AI_PROPERTY_DATA SET `data` = "{jstring}" WHERE ID = "{p.id}";',
        select=False,
    )

    print(f"UPDATED ID {p.id}")
