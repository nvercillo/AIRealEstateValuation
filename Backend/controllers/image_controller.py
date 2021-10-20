import sys
import base64

sys.path.insert(0, "..")  # import parent folder
from models import Image

from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))


class ImageController:
    
    INVALID_IMAGE_ID = "---invalid---"
    
    def __init__(self):
        self.image = Image(start_engine=True)
    
    def get_images_ids_for_property(self, property_id):        
        res = self.image._select_from_where("`id`", "`PROPERTY-IMAGES`", f'`property_id` = "{property_id}"')
        return [str(r[0]) for r in res ]

    def get_image_by_id(self, id):
        if id == self.INVALID_IMAGE_ID : # no houses exist
            file_name = f"static/images/greyhouse.png"
            f = open(file_name, "rb")
            image_binary = f.read()
            return base64.b64encode(image_binary)

        else:
            images = self.image._select_from_where("`raw_image_binary`", "`PROPERTY-IMAGES`", f'ID = "{id}"' )       
            return base64.b64encode(images[0][0])

res = ImageController().get_image_by_id("---invalid---")

