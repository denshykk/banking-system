import src
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()


@app.before_first_request
def create_tables():
    db.create_all()
    src.models.Role(name='user').save_to_db()
    src.models.Role(name='admin').save_to_db()
