from src.app import app, auth
from decimal import Decimal
from flask_restful import reqparse
from src.models import User, Role
from src.models import Account
from src.utils.exception_wrapper import handle_error_format
from src.utils.exception_wrapper import handle_server_exception


@app.route('/accounts/<userId>', methods=['POST'])
@auth.login_required(role='admin')
@handle_server_exception
def create_account(userId: int):
    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    account = Account(
        balance=0,
        userId=userId
    )

    account.save_to_db()

    return Account.to_json(account)


@app.route('/accounts', methods=['POST'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def create_account_for_authorized_user():
    username = auth.current_user()
    user = User.get_by_username(username)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    account = Account(
        balance=0,
        userId=user.id
    )

    account.save_to_db()

    return Account.to_json(account)


@app.route('/accounts/<accountId>', methods=['GET'])
@auth.login_required(role='admin')
@handle_server_exception
def get_account_by_id(accountId: int):
    account = Account.get_by_id(accountId)

    if not account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    return Account.to_json(account)


@app.route('/users/accounts/<userId>', methods=['GET'])
@auth.login_required(role='admin')
@handle_server_exception
def get_user_accounts(userId: int):
    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    return [Account.to_json(account) for account in user.accounts]


@app.route('/users/accounts', methods=['GET'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def get_authorized_user_accounts():
    username = auth.current_user()
    user = User.get_by_username(username)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    return [Account.to_json(account) for account in user.accounts]


@app.route('/accounts/<accountId>', methods=['PUT'])
@auth.login_required(role='admin')
@handle_server_exception
def update_account_by_id(accountId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('balance', type=Decimal, help='balance can not be blank', required=True)

    data = parser.parse_args()
    balance = data['balance']

    if balance <= 0:
        return handle_error_format('Balance must be positive number.',
                                   'Field \'balance\' in the request body.'), 400

    account = Account.get_by_id(accountId)

    if not account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    account.balance = account.balance + balance
    Account.save_to_db(account)

    return Account.to_json(account)


@app.route('/accounts/<accountId>', methods=['DELETE'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def delete_account_by_id(accountId: int):
    username = auth.current_user()
    user = User.get_by_username(username)

    admin = Role.get_by_name('admin')
    if admin in user.roles:
        return Account.delete_by_id(accountId)

    account_to_delete = Account.get_by_id(accountId)
    if account_to_delete not in user.accounts:
        return handle_error_format('You do not have account with that id',
                                   'Field \'accountId\' in path parameters'), 400

    return Account.delete_by_id(accountId)


@app.route('/accounts/<fromAccountId>/transfer-to/<toAccountId>', methods=['POST'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def transfer_to_account(fromAccountId: int, toAccountId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('amount', type=Decimal, help='Amount can not be blank', required=True)

    data = parser.parse_args()
    amount = data['amount']

    if amount <= 0:
        return handle_error_format('Balance must be positive number.',
                                   'Field \'amount\' in the request body.'), 400

    from_account = Account.get_by_id(fromAccountId)

    if not from_account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    username = auth.current_user()
    user = User.get_by_username(username)
    admin = Role.get_by_name('admin')

    if from_account not in user.accounts:
        if admin not in user.roles:
            return handle_error_format('You do not have access to this account.',
                                       'Field \'fromAccountId\' in path parameters.'), 400

    to_account = Account.get_by_id(toAccountId)

    if not to_account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    if from_account.balance < amount:
        return handle_error_format('Moneyless?',
                                   'Field \'amount\' in the request body.'), 400

    from_account.balance = from_account.balance - amount
    to_account.balance = to_account.balance + amount

    Account.save_to_db(from_account)
    Account.save_to_db(to_account)

    return {
        'userId': from_account.id,
        'toUserId': to_account.id,
        'amount': amount
    }
