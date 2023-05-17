from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = getenv('FLASK_SECRET')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS') in ['True']

app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS') in ['True']
app.config['MAIL_USE_SSL'] = bool(getenv('MAIL_USE_SSL'))
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_USERNAME')

cors = CORS(app, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
admin = Admin(app, name='Manage bank entities', template_mode='bootstrap3')
mail = Mail(app)
