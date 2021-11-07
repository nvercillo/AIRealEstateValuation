import sys
import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.types import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from models import db, DB_CONNECTIONS  # import from __init__ file

sys.path.insert(0, "..")  # import parent folder
from utils.abstract import AbstractBaseClass, abstractmethod
from utils.data_structures.db_connections_q import DatabaseConnectionsQueue


class BaseModel(AbstractBaseClass):
    db_connections = None

    @abstractmethod
    def _query_by_id(self, id):
        pass

    @abstractmethod
    def _query_by_ids(self, id):
        pass

    @abstractmethod
    def _query_all(self):
        pass

    def initialize(self):

        assert os.environ["DB_URI"] is not None, print("INVALID DB_URI")

        self.engine = create_engine(
            os.environ["PRODUCTION_DB_URI"],
            echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __as_small_dict__(self):
        pass

    def __as_dict__(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
            and not callable(key)
            and "_sa_instance" not in key
        }

    def _select_from_where_str(self, attributes, relation, condition, distinct=None):
        return f"SELECT {'' if not distinct else 'DISTINCT'} {attributes} FROM {relation} WHERE {condition};"

    def _select_from_where(self, attributes, relation, condition, distinct=None):
        return self._select_query(
            self._select_from_where_str(attributes, relation, condition, distinct)
        )

    def _select_query(self, query_str):
        return DB_CONNECTIONS._query(query_string=query_str)

    def _insert(self, bulk_list):
        for obj in bulk_list:
            self.session.add(obj)
        self.session.commit()

    def commit(self):
        self.session.commit()
