import os
import uuid
from sqlalchemy import Integer, Text
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

from utils.data_structures.sql_object import (
    AttributeValue,
    Filter,
    Attributes,
    Operator,
)
from models.base_model import BaseModel
from . import db  # import from __init__ file


class Property(BaseModel):

    __tablename__ = "AI_PROPERTY_DATA"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(255), index=True)
    longitude = db.Column(db.Numeric(9, 6), index=True)
    latitude = db.Column(db.Numeric(9, 6), index=True)
    sold_price = db.Column(db.Float)
    soldOn = db.Column(db.DateTime)
    soldDate = db.Column(db.DateTime)
    listedOn = db.Column(db.DateTime)
    style = db.Column(db.String(255))
    data = db.Column(Text)
    property_type = db.Column(db.String(35))
    square_footage = db.Column(db.String(10))
    num_bedrooms = db.Column(Integer)
    num_dens = db.Column(Integer)
    parking_spots = db.Column(Integer)
    num_bathrooms = db.Column(Integer)

    def __init__(
        self,
        address=None,
        longitude=None,
        latitude=None,
        sold_price=None,
        soldOn=None,
        soldDate=None,
        listedOn=None,
        style=None,
        data=None,
        property_type=None,
        square_footage=None,
        num_bedrooms=None,
        num_dens=None,
        parking_spots=None,
        num_bathrooms=None,
        skip_creation=False,
    ):

        self.address = address
        self.sold_price = sold_price
        self.soldOn = soldOn
        self.soldDate = soldDate
        self.listedOn = listedOn
        self.num_bathrooms = num_bathrooms
        self.longitude = longitude
        self.latitude = latitude
        self.style = style
        self.num_bedrooms = num_bedrooms
        self.num_dens = num_dens
        self.square_footage = square_footage
        self.property_type = property_type
        self.parking_spots = parking_spots
        self.data = data

        if not skip_creation:
            self._create_self(self)

    @staticmethod
    def _get_columns() -> list:
        ordered_cols = [
            "id",
            "address",
            "longitude",
            "latitude",
            "sold_price",
            "soldOn",
            "soldDate",
            "listedOn",
            "style",
            "data",
            "property_type",
            "square_footage",
            "num_bedrooms",
            "num_dens",
            "parking_spots",
            "num_bathrooms",
        ]
        return ordered_cols

    def __as_small_dict__(self):

        return {
            "address": str(self.address),
            "id": str(self.id),
            "lng": float(self.longitude),
            "lat": float(self.latitude),
            "style": str(self.style),
            "sold_price": str(self.sold_price),
            "property_type": str(self.property_type),
            "square_footage": str(self.square_footage),
            "num_bedrooms": int(self.num_bedrooms),
            "num_bathrooms": int(self.num_bathrooms),
            "num_dens": int(self.num_dens),
            "parking_spots": int(self.parking_spots),
        }

    def __repr__(self):
        return f"< id {self.id}, price {self.sold_price}, style {self.style} >"

    def __str__(self):
        return f"< id {self.id}, price {self.sold_price}, style {self.style} >"

    def _query_by_coord_range_and_filter(
        self, lng_above, lng_below, lat_above, lat_below, filters: list = []
    ):
        """Function gets all nodes within a range of two long and lats"""

        conditions = [
            Filter(Attributes("latitude"), Operator(">"), AttributeValue(lat_below)),
            Filter(Attributes("latitude"), Operator("<"), AttributeValue(lat_above)),
            Filter(Attributes("longitude"), Operator("<"), AttributeValue(lng_above)),
            Filter(Attributes("longitude"), Operator(">"), AttributeValue(lng_below)),
        ]

        conditions.extend(filters)

        res = self._select_from_where_join(
            attributes=Attributes("*"),
            relation=self.__tablename__,
            conditions=conditions,
        )

        return res
