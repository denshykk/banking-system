from flask_admin.contrib import sqla
from flask import request

from src.app import auth, admin, db
from src.models import User, Account, Role


@auth.verify_password
def verify_password(username, password):
    user = User.get_by_username_or_email(username)

    if user and User.verify_hash(password, user.password):
        return username


@auth.get_user_roles
def get_user_roles(user):
    user_entity = User.get_by_username_or_email(user)

    if not user_entity:
        return None

    return [role.name for role in user_entity.roles]


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        auth_header = request.authorization

        if auth_header:
            user = User.get_by_username_or_email(auth_header.username)
            admin = Role.get_by_name('admin')
            if User.verify_hash(auth_header.password, user.password) and admin in user.roles:
                return True

        return False


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Account, db.session))
