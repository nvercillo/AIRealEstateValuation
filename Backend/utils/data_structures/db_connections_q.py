import re
import time
from sqlalchemy import exc
from sqlalchemy.exc import ResourceClosedError
from .heap import Heap
import os
from threading import Lock
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

        def _is_dead(self):
            return self.connection.closed

    COUNT_TO_PURGE = 10

    def __init__(self, capacity):
        super().__init__(capacity, self.DatabaseConnectionNode)
        self.count_to_purge = self.COUNT_TO_PURGE
        self.mutex = Lock()

    def decrement_count(self):
        self.mutex.acquire()
        self.count_to_purge -= 1
        count = self.count_to_purge
        self.mutex.release()

        if count <= 0:
            self.purge_dead_nodes()

        self.mutex.acquire()
        self.count_to_purge = self.COUNT_TO_PURGE
        self.mutex.release()

    def _query(self, query_string):
        self.decrement_count()

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
