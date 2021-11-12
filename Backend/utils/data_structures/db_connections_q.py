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
    pool_pre_ping=True
)


class DatabaseConnectionsQueue(Heap):
    class DatabaseConnectionNode(Heap.HeapNode):
        MAX_CONNECTION_TIME = 2 # in seconds
        def __init__(self, ) -> None:
            self.sortable_value = time.time() # set to inital
            self.connection = db_engine.connect()
            self.available = True

        def __exit__(self):
            try:
                if not self.connection.closed:
                    print(f"Closing DB connection {id(self)} ...")
                    self.connection.close()
                    print(f"Closed DB connection {id(self)}")

            except:
                print("HHHHHHHHHHH")
                pass
            
        def _query_on_connection(self, query_string, select=True):
            res = None
            try:
                result_cnx = self.connection.execute(query_string)
                if select:
                    res = result_cnx.fetchall()
            except Exception as err:
                print("ERROR: ", err)
                res = None
            finally:
                return res

        
        def _is_dead(self):
            curr = time.time()
            
            if int(curr - self.sortable_value) > self.MAX_CONNECTION_TIME:
                if not self.node_lock.acquire(blocking=False):
                    return True # time exceeded and lock still
                else:
                    self.node_lock.release()
            
            return False
    
        def __str__(self):
            return f"<DB Conn: time={self.sortable_value}, open={not self.connection.closed} > "
                    

    COUNT_TO_PURGE = 100000000

    def __init__(self, capacity):
        super().__init__(capacity, HeapNodeClass=self.DatabaseConnectionNode)
        self.count_to_purge = self.COUNT_TO_PURGE
        self.mutex = Lock()

    def __exit__(self):
        for e in self.queue:
            e.__exit__()
    
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

    def _query(self, query_string, select=True):
        self.decrement_count()
        node = self._find_avalible()
        if node is None:
            print("Unable to find available node during timeout period")
            return 
            # raise Exception("Unable to find available node during timeout period")

        query_result = node._query_on_connection(query_string, select)
        print(query_result)
        if self._update_node_val(node, time.time()):
            # print(query_result)
            return query_result

        else:
            print("Failed to update node and heapify queue")
            return
            raise Exception("Failed to update node and heapify queue")
