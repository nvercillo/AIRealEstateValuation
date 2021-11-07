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
        blob_index,
        image_id,
        raw_image_binary,
        start_engine=False,
    ):

        BaseModel.initialize(self)

        if not start_engine:
            self.blob_index = blob_index
            self.foreign_id = image_id
            self.raw_image_binary = raw_image_binary
