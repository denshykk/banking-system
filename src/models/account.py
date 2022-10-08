from src.app import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.DECIMAL, nullable=False)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
