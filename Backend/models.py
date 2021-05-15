import os 
import uuid
import psycopg2
from flask import Flask, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload, load_only
from sqlalchemy.dialects.postgresql import UUID

# from server import db  # UNCOMMENT WHEN RUNNING MIGRATION
# if __name__ =="__main__":
# from server import db
#     print("SDFSDFS")
# else:
db = SQLAlchemy()
    

class Property(db.Model):
    __tablename__ = 'PROPERTIES'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(255), index=True)
    longitude = db.Column(db.Numeric(9,6), index=True)
    latitude = db.Column(db.Numeric(9,6), index=True)
    sold_price = db.Column(db.Float)
    soldOn = db.Column(db.DateTime)
    soldDate = db.Column(db.DateTime)
    listedOn = db.Column(db.DateTime)
    style = db.Column(db.String(255))
    data = db.Column(JSON)

    def __init__(self, address, sold_price, soldOn,
    soldDate, listedOn, longitude, latitude, style, data):
        self.address = address
        self.sold_price = sold_price
        self.soldOn = soldOn
        self.soldDate =soldDate
        self.listedOn = listedOn
        self.style = style
        self.longitude = longitude
        self.latitude = latitude
        self.data = data
        

    def __as_dict__(self):
        return {key:value for key, value in 
            self.__dict__.items() if not key.startswith('__') 
            and not callable(key) and '_sa_instance' not in key}


    @staticmethod   
    def _query_by_coords(lgn, lat):
        engine = create_engine(os.environ["DB_URI"], echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(Property).all()
        return res

    @staticmethod   
    def _query_by_id(id):
        engine = create_engine(os.environ["DB_URI"], echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(Property).get(id)
        return res

    @staticmethod   
    def _query_all():
        engine = create_engine(os.environ["DB_URI"], echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(Property).all()
        return res

    
    @staticmethod
    def _insert(bulk_list):
        assert os.environ['DB_URI'] == "postgresql://ijnykwiczlfsrl:2b76aead17ba334800f1360d3c6f37c9f128be22965e08bc23445aa0a9f5cfbc@ec2-54-160-96-70.compute-1.amazonaws.com:5432/d85hoc3itaj780", \
            print("GOT ", os.environ['DB_URI'])
        engine = create_engine(os.environ["DB_URI"], echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        for obj in bulk_list:
            session.add(obj)
        session.commit()


    def __as_small_dict__(self):
        return {
            "address" : str(self.address),
            "id" : str(self.id),
            "lgn": float(self.longitude),
            "lat" : float(self.latitude)
        }
    def __repr__(self):
        return f'<address {self.address}, id {self.id}>'

    def __str__(self):
        return f'<address {self.address}, id {self.id}, lgn {self.longitude}, lat {self. latitude}>'




