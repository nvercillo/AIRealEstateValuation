import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql.base import INTERVAL
from sqlalchemy.types import BLOB, SMALLINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from . import db  # import from __init__ file


class ImageBlob(db.Model, BaseModel):

    __tablename__ = "IMAGE_BLOB"

    # mulit valued key pair
    blob_index = db.Column(SMALLINT, primary_key=True)  # primary key
    image_id = db.Column(
        UUID(as_uuid=True), index=True, primary_key=True
    )  # primary key

    raw_image_binary = db.Column(BLOB)

    def __init__(
        self,
        blob_index=None,
        image_id=None,
        raw_image_binary=None,
        skip_creation=False,
    ):

        self.blob_index = blob_index
        self.image_id = image_id
        self.raw_image_binary = raw_image_binary

        if not skip_creation:
            self._create_self(self)

    @staticmethod
    def _get_columns() -> list:
        return ["blob_index", "image_id", "raw_image_binary"]

    def __as_small_dict__(self):
        return {
            "blob_index": str(self.blob_index),
            "image_id": str(self.image_id),
        }

    def __repr__(self):
        return f"< IMAGE_BLOB blob_index {self.blob_index}, image_id {self.image_id} >"

    def __str__(self):
        return f"< IMAGE_BLOB blob_index {self.blob_index}, image_id {self.image_id} >"
