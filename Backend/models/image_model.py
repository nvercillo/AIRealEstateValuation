import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.types import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from models.base_model import BaseModel
from models import db  # import from __init__ file
from utils.data_structures.sql_object import Filter, Attributes


class Image(BaseModel, db.Model):

    __tablename__ = "PROPERTY_IMAGES"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = db.Column(UUID(as_uuid=True), index=True)
    num_blobs = db.Column(Integer)  # not null TODO

    def __init__(
        self,
        id=None,
        property_id=None,
        num_blobs=None,
        skip_creation=False,
    ):

        self.id = id if id is not None else uuid.uuid4()
        self.property_id = property_id
        self.num_blobs = num_blobs

        if not skip_creation:
            self._create_self(self)

    @staticmethod
    def _get_columns() -> list:
        return ["id", "property_id", "num_blobs"]

    def __as_small_dict__(self):
        return {"id": str(self.id), "property_id": str(self.property_id)}

    def __repr__(self):
        return f"< Image id {self.id}, num_blobs {self.num_blobs} >"

    def __str__(self):
        return f"< Image id {self.id}, num_blobs {self.num_blobs} >"
