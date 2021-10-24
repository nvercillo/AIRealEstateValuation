import os
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Integer, create_engine
from sqlalchemy.sql.expression import update
from sqlalchemy.types import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()


class Property(db.Model):

    __tablename__ = "AI-PROPERTIES-DATA"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(255), index=True)
    longitude = db.Column(db.Numeric(9, 6), index=True)
    latitude = db.Column(db.Numeric(9, 6), index=True)
    sold_price = db.Column(db.Float)
    soldOn = db.Column(db.DateTime)
    soldDate = db.Column(db.DateTime)
    listedOn = db.Column(db.DateTime)
    style = db.Column(db.String(255))
    num_bedrooms = db.Column(Integer)
    num_bathrooms = db.Column(Integer)
    num_dens = db.Column(Integer)
    square_footage = db.Column(db.String(10))
    property_type = db.Column(db.String(35))
    parking_spots = db.Column(Integer)
    data = db.Column(JSON)

    def __init__(
        self,
        address=None,
        sold_price=None,
        soldOn=None,
        soldDate=None,
        listedOn=None,
        longitude=None,
        latitude=None,
        style=None,
        num_bedrooms=None,
        num_dens=None,
        num_bathrooms=None,
        square_footage=None,
        property_type=None,
        parking_spots=None,
        data=None,
        start_engine=False,
    ):

        assert os.environ["DB_URI"] is not None, print("INVALID DB_URI")

        self.engine = create_engine(
            os.environ["PRODUCTION_DB_URI"],
            echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        if not start_engine:
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

    def __as_dict__(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
            and not callable(key)
            and "_sa_instance" not in key
        }

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

    """ Function gets all nodes within a range of two long and lats """

    def _query_by_coord_range_and_filter(
        self, lng_above, lng_below, lat_above, lat_below, filters=False
    ):

        if not filters:
            res = (
                self.session.query(Property)
                .filter(
                    Property.latitude > lat_below,
                    Property.latitude < lat_above,
                    Property.longitude < lng_above,
                    Property.longitude > lng_below,
                )
                .all()
            )

        else:
            res = (
                self.session.query(Property)
                .filter(
                    Property.latitude > lat_below,
                    Property.latitude < lat_above,
                    Property.longitude < lng_above,
                    Property.longitude > lng_below,
                    Property.style == filters["style"],
                )
                .all()
            )

        return res

    def _query_by_id(self, id):
        res = self.session.query(Property).get(id)
        return res

    def _query_by_ids(self, ids):
        res = self.session.query(Property).filter(Property.id.in_(ids)).all()
        return res

    def _query_all(self):
        res = self.session.query(Property).all()
        return res

    def _insert(self, bulk_list):
        for obj in bulk_list:
            self.session.add(obj)
        self.session.commit()

    def commit(self):
        self.session.commit()


class Image(db.Model):

    __tablename__ = "PROPERTY-IMAGES"

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

        assert os.environ["DB_URI"] is not None, print("INVALID DB_URI")

        self.engine = create_engine(
            os.environ["PRODUCTION_DB_URI"],
            echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
        )

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

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

    def _select_from_where(self, attributes, relation, condition, distinct=None):
        with self.engine.connect() as con:

            result = con.execute(
                f"SELECT {'' if not distinct else 'DISTINCT'} {attributes} FROM {relation} WHERE {condition};"
            )

            return result.fetchall()

    def _insert(self, bulk_list):
        for obj in bulk_list:
            self.session.add(obj)
        self.session.commit()

    def commit(self):
        self.session.commit()
