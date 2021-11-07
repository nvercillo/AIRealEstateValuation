import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.types import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from models.base_model import BaseModel
from models import db  # import from __init__ file


class Image(BaseModel, db.Model):

    __tablename__ = "PROPERTY_IMAGES"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = db.Column(UUID(as_uuid=True), index=True)
    raw_image_binary = db.Column(BLOB)

    def __init__(
        self,
        id=None,
        property_id=None,
        raw_image_binary=None,
        start_engine=False,
    ):
        BaseModel.initialize(self)

        if not start_engine:
            self.id = id
            self.property_id = property_id
            self.raw_image_binary = raw_image_binary

    def __as_dict__(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
            and not callable(key)
            and "_sa_instance" not in key
        }

    def __as_small_dict__(self):
        return {"id": str(self.id), "property_id": str(self.property_id)}

    def __repr__(self):
        return f"< id {self.id}, property_id {self.property_id} >"

    def __str__(self):
        return f"< id {self.id}, property_id {self.property_id} >"

    def _query_by_id(self, id):
        res = self.session.query(Image).get(id)
        return res

    def _query_all(self):
        res = self.session.query(Image).all()
        return res


# engine = create_engine(
#     os.environ["PRODUCTION_DB_URI"],
#     echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
# )
# con = engine.connect()
# result = con.execute("SELECT * FROM PROPERTY_IMAGES LIMIT 10")
# import time

# time.sleep(5)
# print(con.closed)
# con.close()
# print(con.closed)
