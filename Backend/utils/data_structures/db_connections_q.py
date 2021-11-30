import re
import time
from flask.app import Flask
from sqlalchemy import exc
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.orm import query
from .heap import Heap
import os
import MySQLdb
from threading import Lock, current_thread
from sqlalchemy import create_engine

import mysql.connector
import MySQLdb._mysql
import sys

sys.path.insert(0, "../..")
from utils.app_config import AppConfig
from utils.utility_functions import safeprint


# cnx = mysql.connector.connect(**AppConfig.db_config())


class DatabaseConnectionsQueue(Heap):
    class DatabaseConnectionNode(Heap.HeapNode):
        MAX_CONNECTION_TIME = 100  # in seconds

        def __init__(
            self,
        ) -> None:
            self.node_lock = Lock()

            self.sortable_value = time.time()  # set to inital
            try:
                self.connection = mysql.connector.connect(**AppConfig.db_config())
                self.init_failed = False
            except Exception as err:

                safeprint(f"ERROR: {err}")
                self.init_failed = True

        def __exit__(self):
            try:
                if not self.connection.closed:
                    safeprint(f"Closing DB connection {id(self)} ...")
                    self.connection.close()
                    safeprint(f"Closed DB connection {id(self)}.")

            except:
                pass

        def _query_on_connection(self, query_string, query_vals, select=True):
            res = None

            try:
                try:
                    cursor = self.connection.cursor()
                except:
                    self.connection = mysql.connector.connect(**AppConfig.db_config())
                    cursor = self.connection.cursor()

                query_vals = tuple(query_vals)
                cursor.execute(query_string, query_vals)

                if select:
                    res = cursor.fetchall()
                else:
                    self.connection.commit()
            except Exception as err:
                safeprint("ERROR: ", err)
                res = None
            finally:
                return res

        def _is_dead(self):
            curr = time.time()
            if int(curr - self.sortable_value) > self.MAX_CONNECTION_TIME:
                if not self.node_lock.acquire(blocking=False):
                    return True  # time exceeded and lock still
                else:
                    self.node_lock.release()

            return False

        def __str__(self):
            return f"<DB Conn: time={self.sortable_value}, open={not self.connection.closed} > "

    COUNT_TO_PURGE = 1000

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
            while self.count_to_purge <= 0:
                self.mutex.acquire()
                purged = self._purge_dead_nodes()
                if purged:
                    self.count_to_purge = self.COUNT_TO_PURGE
                self.mutex.release()

    def _query(self, query_string, query_vals=[], select=True):
        self.decrement_count()
        node = self._find_avalible()
        if node is None:
            safeprint("Unable to find available node during timeout period")
            return
            # raise Exception("Unable to find available node during timeout period")

        query_result = node._query_on_connection(query_string, query_vals, select)
        if self._update_node_val(node, time.time()):
            return query_result

        else:
            safeprint("Failed to update node and heapify queue")
            return
            # raise Exception("Failed to update node and heapify queue")
