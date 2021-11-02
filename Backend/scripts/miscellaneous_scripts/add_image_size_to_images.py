""" 
Description: add byte size to property-images 

"""
import sys

sys.path.insert(0, "../../")  # import parent folder
from models import Image
from server import db
from sqlalchemy.dialects.postgresql import insert

image_model = Image()

with image_model.engine.connect() as con:

    query = con.execute("CREATE TABLE PROPERTY_IMAGES LIKE `PROPERTY-IMAGES` ;")
    query.commit()

    query = con.execute(
        f"ALTER TABLE PROPERTY_IMAGES ADD COLUMN `byte_size` decimal(10);"
    )

    query = con.execute(
        "INSERT INTO PROPERTY_IMAGES (id, property_id, raw_image_binary, byte_size) SELECT id, property_id, raw_image_binary, OCTET_LENGTH(raw_image_binary) FROM `PROPERTY-IMAGES`;"
    )
