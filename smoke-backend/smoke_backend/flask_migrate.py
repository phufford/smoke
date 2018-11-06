from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, Migrate Command

from app import app #import the app object from the app module
from app import db 


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if _name_ == '_main_':
    manager.run()