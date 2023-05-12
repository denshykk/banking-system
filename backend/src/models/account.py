from src.app import db
from src.utils.exception_wrapper import handle_error_format


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(15, 2), nullable=False)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

    def to_json(self):
        return {
            'id': self.id,
            'balance': self.balance,
            'user_id': self.userId
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, account_id):
        return cls.query.filter_by(id=account_id).first()

    @classmethod
    def delete_by_id(cls, account_id):
        account = Account.get_by_id(account_id)

        if not account:
            return handle_error_format('Account with such id does not exist.',
                                       'Field \'accountId\' in path parameters.'), 404

        account_json = Account.to_json(account)

        cls.query.filter_by(id=account_id).delete()
        db.session.commit()

        return account_json
