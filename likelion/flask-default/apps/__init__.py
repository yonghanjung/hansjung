"""
Initialize Flask app

"""
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask('apps')
app.config.from_object('apps.settings.Production')

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db',MigrateCommand)


import views