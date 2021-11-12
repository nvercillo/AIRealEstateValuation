# from threading import Thread
# from time import thread_time, sleep
# from flask_sqlalchemy import SQLAlchemy
# from utils.data_structures.db_connections_q import DatabaseConnectionsQueue

# db = SQLAlchemy()

# DB_CONNECTIONS = DatabaseConnectionsQueue(
#     capacity=2
# )  # max 100 number of db connections


# s = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "02a17044-b120-4723-88d8-d98b41908dcc";'

# N = 3

# thread_pool = []

# for i in range(N):
#     thread = Thread(target=DB_CONNECTIONS._query, args=(s,))
#     thread.start()


# sleep(10)
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
#     capacity=2
# )  # max 100 number of db connections


# s = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "--this-property-id-doesnt-exist ";'

# N = 1

# thread_pool = []

# for i in range(N):
#     thread = Thread(target=DB_CONNECTIONS._query, args=(s,))
#     thread.start()


# timeout = 10

# sleep(2)

# print("starting search ... ")
# while timeout:
#     if DB_CONNECTIONS.queue[0].node_lock.acquire():
#         print(f"Got lock at {10 - timeout} s" )
        
#         DB_CONNECTIONS.queue[0].node_lock.release()

#         DB_CONNECTIONS._query(s)
#         break
        
    


# sleep(20)
# for t in thread_pool:
#     t.join()


# DB_CONNECTIONS.__exit__()


# # for e in DB_CONNECTIONS.queue:
# #     e.__exit__()




# from threading import Thread
# from time import thread_time, sleep
# from flask_sqlalchemy import SQLAlchemy
# from utils.data_structures.db_connections_q import DatabaseConnectionsQueue

# db = SQLAlchemy()

# DB_CONNECTIONS = DatabaseConnectionsQueue(
#     capacity=1
# )  # max 100 number of db connections


# s1 = 'SELECT  `id`, `byte_size` FROM PROPERTY_IMAGES WHERE `property_id` = "02a17044-b120-4723-88d8-d98b41908dcc";'

# s = 'SELECT  * FROM PROPERTY_IMAGES as p1 JOIN PROPERTY_IMAGES as p2 on p1.`id` = p2.`id`;'

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
