from src.app import db
from src.models import Account
from passlib.hash import pbkdf2_sha256 as sha256
from src.utils.exception_wrapper import handle_error_format


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('user', lazy='dynamic'))

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'accountIds': [account.id for account in self.accounts],
            'roles': [role.name for role in self.roles],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, userId):
        return User.query.filter_by(id=userId).first()

    @classmethod
    def get_by_username_or_id(cls, identifier):
        return User.query.filter((User.id == identifier) | (User.username == identifier)).first()

    @classmethod
    def get_by_username_or_email(cls, identifier):
        return User.query.filter((User.email == identifier) | (User.username == identifier)).first()

    @classmethod
    def delete_by_identifier(cls, identifier):
        user = User.get_by_username_or_id(identifier)

        if not user:
            return handle_error_format('User with such id/username does not exist.',
                                       'Field \'userId/username\' in path parameters.'), 404

        user_json = User.to_json(user)
        User.query.filter_by(id=user.id).delete()
        db.session.commit()
        return user_json
