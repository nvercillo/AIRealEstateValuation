import sys
from .lru_cache import LRUCache


sys.path.insert(0, "../../")  # import parent folder
from controllers.image_controller import ImageController
from utils.utility_functions import split_str_into_n_sized_parts
from constants import MAX_NUM_BYTES_PER_PKT


class ImageCache(LRUCache):

    _type = "Image"

    def __init__(self, capacity: int):
        super(ImageCache, self).initialize(capacity=capacity)

    def get_type(self):
        return self._type

    def store_image(self, image_id):
        raw_image_binary = ImageController().get_image_by_id(image_id)

        img_slices = split_str_into_n_sized_parts(
            raw_image_binary, MAX_NUM_BYTES_PER_PKT
        )
        self.put(image_id, img_slices)

    def get_image_slice(self, image_id, img_index):
        return self.get(image_id)[img_index]
