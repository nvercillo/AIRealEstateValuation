from flask_sqlalchemy import SQLAlchemy
from utils.data_structures.db_connections_q import DatabaseConnectionsQueue

db = SQLAlchemy()


# DB_CONNECTIONS = DatabaseConnectionsQueue(
#     capacity=1
# )  # max 150 number of db connections
