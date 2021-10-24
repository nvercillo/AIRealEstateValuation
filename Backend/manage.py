import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from server import app, db

from utils.app_config import AppConfig

app = AppConfig(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
