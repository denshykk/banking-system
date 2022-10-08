from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.models.user import User
from src.models.account import Account


@app.route('/api/v1/hello-world-25')
def hello_world():
    return "Hello World 25"


if __name__ == '__main__':
    app.run(debug=True)
