import base64

from flask_admin.contrib import sqla
from flask import request, session, abort

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
        if (not "authData" in session and not request.args.get('authorization')):
            abort(404)

        if ("authData" in session):
            username = base64.b64decode(session["authData"]).__str__().split("\'")[1].split(":")[0]
            password = base64.b64decode(session["authData"]).__str__().split("\'")[1].split(":")[1]

            user = User.get_by_username_or_email(username)
            admin = Role.get_by_name('admin')
            if User.verify_hash(password, user.password) and admin in user.roles:
                return True

        auth_header = request.args.get('authorization').split(" ")[1]
        username = base64.b64decode(auth_header).__str__().split("\'")[1].split(":")[0]
        password = base64.b64decode(auth_header).__str__().split("\'")[1].split(":")[1]

        if auth_header:
            user = User.get_by_username_or_email(username)
            admin = Role.get_by_name('admin')
            if User.verify_hash(password, user.password) and admin in user.roles:
                session["authData"] = request.args.get('authorization').split(" ")[1]
                return True

        return False


class UserModelView(AdminModelView):
    column_list = ('id', 'username', 'first_name', 'last_name', 'email', 'roles', 'accounts', 'overall_balance')
    column_searchable_list = ('id', 'username', 'first_name', 'last_name', 'email')

    column_formatters = {
        'roles': lambda v, c, m, p: [role.name for role in m.roles],
        'accounts': lambda v, c, m, p: [account.id for account in m.accounts],
        'overall_balance': lambda v, c, m, p: sum([account.balance for account in m.accounts])
    }


class AccountModelView(AdminModelView):
    column_list = ('id', 'balance', 'userId', 'user.username')
    column_searchable_list = ('id', 'balance', 'userId')


admin.add_view(UserModelView(User, db.session))
admin.add_view(AccountModelView(Account, db.session))
