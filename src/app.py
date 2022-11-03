from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_restful import reqparse

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

import src.models.user
import src.models.account
import  src.route.users
import  src.route.accounts

@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello World 15"


@app.before_request
def create_tables():
    db.create_all()
