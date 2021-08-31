import os
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID

# from server import db  # UNCOMMENT WHEN RUNNING MIGRATION
# if __name__ =="__main__":
# from server import db
#     print("SDFSDFS")
# else:
db = SQLAlchemy()


class Property(db.Model):
    __tablename__ = "PROPERTIES"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(255), index=True)
    longitude = db.Column(db.Numeric(9, 6), index=True)
    latitude = db.Column(db.Numeric(9, 6), index=True)
    sold_price = db.Column(db.Float)
    soldOn = db.Column(db.DateTime)
    soldDate = db.Column(db.DateTime)
    listedOn = db.Column(db.DateTime)
    style = db.Column(db.String(255))
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
        data=None,
        start_engine=False,
    ):

        assert os.environ["DB_URI"] is not None, print("INVALID DB_URI")

        engine = create_engine(
            os.environ["PRODUCTION_DB_URI"],
            echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()

        if not start_engine:
            self.address = address
            self.sold_price = sold_price
            self.soldOn = soldOn
            self.soldDate = soldDate
            self.listedOn = listedOn
            self.style = style
            self.longitude = longitude
            self.latitude = latitude
            self.data = data

    def __as_dict__(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
            and not callable(key)
            and "_sa_instance" not in key
        }

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

    def __as_small_dict__(self):
        return {
            "address": str(self.address),
            "id": str(self.id),
            "lng": float(self.longitude),
            "lat": float(self.latitude),
        }

    def __repr__(self):
        return f"< id {self.id}, price {self.sold_price}, style {self.style} >"

    def __str__(self):
        return f"< id {self.id}, price {self.sold_price}, style {self.style} >"
