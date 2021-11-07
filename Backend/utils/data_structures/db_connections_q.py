import re
import time
from sqlalchemy import exc
from sqlalchemy.exc import ResourceClosedError
from .heap import Heap
import os
from sqlalchemy import create_engine

db_engine = create_engine(
    os.environ["PRODUCTION_DB_URI"],
    echo=not (os.environ["PRODUCTION"] and os.environ["PRODUCTION"] == "True"),
)


class DatabaseConnectionsQueue(Heap):
    class DatabaseConnectionNode(Heap.HeapNode):
        def __init__(self) -> None:
            self.sortable_value = 0  # set each node to 0
            self.connection = db_engine.connect()
            self.available = True

        def _query_on_connection(self, query_string):
            try:
                result_cnx = self.connection.execute(query_string)
                res = result_cnx.fetchall()
            except Exception as err:
                print("ERROR: ", err)
                res = None
            finally:
                return res

    def __init__(self, capacity):
        super().__init__(capacity, self.DatabaseConnectionNode)

    def _query(self, query_string):

        node = self._find_avalible()
        if node is None:
            raise Exception("Unable to find available node during timeout period")

        print("res")
        query_result = node._query_on_connection(query_string)
        print("res", query_result)

        if self._update_node_val(node, time.time()):
            return query_result

        else:
            raise Exception("Failed to update node and heapify queue")
