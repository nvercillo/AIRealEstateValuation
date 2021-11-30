# from threading import Thread
# from time import thread_time, sleep

# from sqlalchemy.log import class_logger
# from flask_sqlalchemy import SQLAlchemy
# from utils.data_structures.db_connections_q import DatabaseConnectionsQueue
# import mysql.connector
# import sys

# sys.path.insert(0, "../..")
# from utils.app_config import AppConfig


# cnx = mysql.connector.connect(**AppConfig.db_config())

# cursor = cnx.cursor()

# cursor.execute(
#     'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "0f71385b-sdfsdfd";'
# )
# rows = cursor.fetchall()

# print(rows)


# def connections():

#     cnxs = []
#     for i in range(30):
#         print(f"connecting {i}")
#         try:
#             cnxs.append(mysql.connector.connect(**AppConfig.db_config()))
#         except Exception as err:
#             print(err)

#     print("finished", len(cnxs), "\n\n\n")

#     for c in cnxs:
#         c.close()


# cnxs = []
# for i in range(30):
#     print(f"connecting {i}")
#     try:
#         cnxs.append(mysql.connector.connect(**AppConfig.db_config()))
#     except Exception as err:
#         print(err)

# cursor = cnxs[0].cursor()
# print("finished", len(cnxs))

# cursor.execute(
#     "SELECT IFNULL(usr,'All Users') user,IFNULL(hst,'All Hosts') host,COUNT(1) Connections FROM ( SELECT user usr,LEFT(host,LOCATE(':',host) - 1) hst FROM information_schema.processlist WHERE user NOT IN ('system user','root')) A GROUP BY usr,hst WITH ROLLUP;"
# )


# for e in cursor:
#     print(e)


# sleep(30)
# for c in cnxs:
#     c.close()


# DB_CONNECTIONS.__exit__()


# for e in DB_CONNECTIONS.queue:
#     e.__exit__()


# from threading import Thread
# from time import thread_time, sleep
# from flask_sqlalchemy import SQLAlchemy
# from utils.data_structures.db_connections_q import DatabaseConnectionsQueue

# db = SQLAlchemy()

# DB_CONNECTIONS = DatabaseConnectionsQueue(
#     capacity=5
# )  # max 100 number of db connections


# s = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "--this-property-id-doesnt-exist ";'
# # s = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES;"

# N = 1

# thread_pool = []

# print(DB_CONNECTIONS.capacity)

# import time

# start = time.time()
# for i in range(6):
#     thread = Thread(target=DB_CONNECTIONS._query, args=(s,))
#     thread.start()


# NEXT ...
# DB_CONNECTIONS._query(s)

# timeout = 10

# sleep(2)

# print("starting search ... ")
# while timeout:
#     if DB_CONNECTIONS.queue[0].node_lock.acquire():
#         print(f"Got lock at {10 - timeout} s")

#         DB_CONNECTIONS.queue[0].node_lock.release()

#         DB_CONNECTIONS._query(s)
#         break


# sleep(20)
# for t in thread_pool:
#     t.join()


# DB_CONNECTIONS.__exit__()


# for e in DB_CONNECTIONS.queue:
#     e.__exit__()


# from threading import Thread
# from time import thread_time, sleep
# from flask_sqlalchemy import SQLAlchemy
# from utils.data_structures.db_connections_q import DatabaseConnectionsQueue

# db = SQLAlchemy()

# DB_CONNECTIONS = DatabaseConnectionsQueue(
#     capacity=1
# )  # max 100 number of db connections


# s1 = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "02a17044-b120-4723-88d8-d98b41908dcc";'

# s = "SELECT  * FROM PROPERTY_IMAGES as p1 JOIN PROPERTY_IMAGES as p2 on p1.`id` = p2.`id`;"

# N = 1
# thread_pool = []


# # DB_CONNECTIONS._query(s)


# for i in range(1):
#     thread = Thread(target=DB_CONNECTIONS._query, args=(s,))
#     thread.start()

# for t in thread_pool:
#     t.join()


# # DB_CONNECTIONS._query(s)
# sleep(4)
# print("purging dead")
# # print(DB_CONNECTIONS._query("show status where `variable_name` = 'Threads_connected';"))
# # DB_CONNECTIONS._purge_dead_nodes()

# # DB_CONNECTIONS._query(s1)

# # sleep(10)


# DB_CONNECTIONS.__exit__()
