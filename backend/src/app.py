from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = 'agjghdaskhglkjsadhgkjsavjksgiuhwkrbv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
admin = Admin(app, name='Manage bank entities', template_mode='bootstrap3')
