from decimal import Decimal
import os
from sqlalchemy import create_engine
from sqlalchemy.types import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from utils.data_structures.db_connections_q import DatabaseConnectionsQueue
from utils.data_structures.sql_object import AttributeValue, JoinCondition
from utils.data_structures.sql_object import (
    Attributes,
    Filter,
    SQLObject,
    Operator,
    AttributeValue,
)


import sys

sys.path.insert(0, "..")  # import parent folder
from utils.abstract import AbstractBaseClass, abstractmethod

from utils.utility_functions import safeprint


class BaseModel(SQLObject, AbstractBaseClass):

    _dev_mode = True
    _db_connections = DatabaseConnectionsQueue(
        capacity=20
    )  # max 150 number of db connections

    @abstractmethod
    @staticmethod
    def _get_columns(self) -> list:
        pass

    def _initialize(self):

        assert os.environ["DB_URI"] is not None, safeprint("INVALID DB_URI")
        assert os.environ["PRODUCTION"] is not None

        # self._dev_mode = False if os.environ["PRODUCTION"] == "True" else True
        # TODO: switch this to debug mode off in production
        self._dev_mode = True

        self.engine = create_engine(
            os.environ["PRODUCTION_DB_URI"],
            echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __as_small_dict__(self):
        pass

    def __as_dict__(self, attributes: Attributes = None):
        if attributes is None:
            res = {
                key: value
                for key, value in self.__dict__.items()
                if not key.startswith("__")
                and not callable(key)
                and "_sa_instance" not in key
            }
        else:
            res = {attr: getattr(self, attr) for attr in attributes.attributes}

        return res

    @staticmethod
    def _process_db_res(obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return obj

    def _select_from_where_join_str(
        self,
        attributes: Attributes,
        relation: str,
        conditions: list = [],  # list of type Filter
        join_condition: JoinCondition = None,
        distinct=False,
        limit=None,
    ):
        if type(conditions) != list:
            conditions = [conditions]
        where_clause = "" if len(conditions) == 0 else "WHERE"
        for i in range(len(conditions)):

            _filter = conditions[i]
            assert "Filter" in str(
                type(_filter)
            ), f"EXPECTED `Filter` TYPE NOT `{type(_filter)}`"

            where_clause += f" {str(_filter)}"
            if i != len(conditions) - 1:
                where_clause += " AND"

        res = (
            f"SELECT {'' if not distinct else 'DISTINCT'} "
            + f"{str(attributes)} FROM {relation} "
            + f"{str(join_condition) if join_condition is not None else ''} "
            + f"{where_clause} "
            + f"{'LIMIT ' + str(limit) if limit is not None else ''};"
        )

        return res

    def _select_from_where_join(
        self,
        attributes: Attributes,
        relation: str,
        conditions: list,
        join_condition: JoinCondition = None,
        distinct=None,
    ):
        res = self._query(
            self._select_from_where_join_str(
                attributes, relation, conditions, join_condition, distinct
            )
        )

        if join_condition is not None:
            return self._map_query_res_to_model(res, attributes, [join_condition.obj2])
        else:
            return self._map_query_res_to_model(res, attributes)

    def _query(self, query_str, query_vals=[], select=True):
        if self._dev_mode:
            safeprint(f"QUERY: '{query_str}',  query_vals", query_vals)

        return self._db_connections._query(
            query_string=query_str, query_vals=query_vals, select=select
        )

    def _create_self(self, obj):
        self._insert(bulk_list=[obj])

    def _insert(self, bulk_list):
        if type(bulk_list) != list:
            bulk_list = [bulk_list]

        attrs = []
        for col in self._get_columns():
            if getattr(bulk_list[0], col) is not None:
                attrs.append(col)

        query_string = f"INSERT INTO {self.__tablename__} ("
        for i in range(len(attrs)):
            query_string += f"`{attrs[i]}`"
            if i != len(attrs) - 1:
                query_string += ", "
        query_string += ") VALUES "

        query_vals = []
        for i, obj in enumerate(bulk_list):
            query_string += "("

            for j, at in enumerate(attrs):
                val = getattr(obj, at)
                try:
                    at_val = AttributeValue(val)
                except:
                    safeprint("FAILED TO INSERT, INCONSISTENT TYPES ACROSS INSERT ARR")
                    return

                query_string += "%s"
                query_vals.append(at_val.val)
                if j != len(attrs) - 1:
                    query_string += ", "

            query_string += ")"
            if i != len(bulk_list) - 1:
                query_string += ", "

        query_string += ";"

        self._query(query_str=query_string, query_vals=query_vals, select=False)

    @staticmethod
    def static_column_map(obj, offset=0) -> dict:
        return {col: i + offset for i, col in enumerate(obj._get_columns())}

    def _column_map(self) -> dict:
        return {col: i for i, col in enumerate(self._get_columns())}

    def _map_query_res_to_model(
        self,
        query_res,
        attributes: Attributes,
        obj_ordered_by_selected_attributes: list = [],
    ):  # Model

        if attributes.attributes is None or attributes.attributes == "*":
            cols = self._get_columns()
            for obj in obj_ordered_by_selected_attributes:
                cols.extend(obj._get_columns())
        else:
            cols = attributes._to_list()

        col_map = self._column_map()

        for obj in obj_ordered_by_selected_attributes:
            col_map.update(
                self.static_column_map(obj, offset=len(col_map))
            )  # update dict with new values

        sorted_cols = sorted(cols, key=lambda ele: col_map[ele])
        results = []

        index_map = {c: i for i, c in enumerate(sorted_cols)}
        Model = self.__class__

        for res in query_res:
            model = Model(skip_creation=True)

            for attr in sorted_cols:
                setattr(model, attr, self._process_db_res(res[index_map[attr]]))

            results.append(model)

        return results

    def _query_by_id(self, id):
        res = self._query(
            self._select_from_where_join_str(
                attributes=Attributes("*"),
                relation=self.__tablename__,
                conditions=[
                    Filter(Attributes("id"), Operator("="), AttributeValue(id))
                ],
            )
        )

        if not len(res):
            return []

        return self._map_query_res_to_model(res, Attributes("*"))[0]

    def _query_by_ids(self, ids):

        res = self._query(
            self._select_from_where_join_str(
                attributes=Attributes("*"),
                relation=self.__tablename__,
                conditions=Filter(
                    Attributes("id"), Operator("IN"), AttributeValue(ids)
                ),
            )
        )

        if not len(res):
            return []

        return self._map_query_res_to_model(res, Attributes("*"))

    def _query_all(self, limit=None):

        attributes = Attributes("*")
        res = self._query(
            self._select_from_where_join_str(
                attributes=attributes, relation=self.__tablename__, limit=limit
            )
        )

        if not len(res):
            return []

        return self._map_query_res_to_model(res, attributes)
