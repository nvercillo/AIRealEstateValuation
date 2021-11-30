from math import ceil
import sys
import base64


sys.path.insert(0, "..")  # import parent folder
from models.image_model import Image
from models.blob_model import ImageBlob
from utils.data_structures.sql_object import (
    Filter,
    Attributes,
    JoinCondition,
    Operator,
    AttributeValue,
)
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), ".env"))


class ImageController:

    INVALID_IMAGE_ID = "---invalid---"
    INVALID_IMAGE_LEN = 11610  # bytes

    def __init__(self):
        self.image = Image(skip_creation=True)

    def get_images_ids_for_property(self, property_id):
        select_attributes = Attributes(["id", "num_blobs"])
        images = self.image._select_from_where_join(
            select_attributes,
            Image.__tablename__,
            Filter(
                Attributes("property_id"), Operator("="), AttributeValue(property_id)
            ),
        )

        if len(images) == 0:
            images.append(
                Image(
                    id=self.INVALID_IMAGE_ID,
                    num_blobs=ceil(self.INVALID_IMAGE_LEN / 64000),
                    skip_creation=True,
                )
            )

        res = [image.__as_dict__(attributes=select_attributes) for image in images]

        return res

    def get_image_by_id(self, id):
        if id == self.INVALID_IMAGE_ID:  # no houses exist
            file_name = f"static/images/greyhouse.png"
            f = open(file_name, "rb")
            image_binary = f.read()
            return image_binary
        else:
            image_slices = self.image._select_from_where_join(
                Attributes("raw_image_binary"),
                Image.__tablename__,
                Filter(Attributes("id"), Operator("="), AttributeValue(id)),
                JoinCondition(
                    obj1=Image(skip_creation=True),
                    obj2=ImageBlob(skip_creation=True),
                    join_on_1=Attributes("id"),
                    join_on_2=Attributes("image_id"),
                    join_operator=Operator("="),
                    join_type=JoinCondition.JoinType.LEFT,
                ),
            )
            byte_size = b""
            for slice in image_slices:
                byte_size += slice.raw_image_binary

            return byte_size
