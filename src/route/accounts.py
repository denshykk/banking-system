from src.app import app
from src.models.account import Account
from src.models.user import User
from datetime import datetime
from flask_restful import reqparse
from werkzeug.exceptions import NotFound
from src.utils.exception_wrapper import handle_server_exception
from src.utils.exception_wrapper import handle_error_format
from decimal import Decimal


@app.route('/accounts', methods=['POST'])
@handle_server_exception
def create_account():
    parser = reqparse.RequestParser()
    parser.add_argument('userId', type=int, help='fullname cannot be blank', required=True)

    data = parser.parse_args()
    user_id = data['userId']

    user = User.get_by_id(user_id)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    account = Account(
        balance=0,
        userId=user_id
    )

    account.save_to_db()

    return Account.to_json(account)


@app.route('/accounts/<accountId>', methods=['GET'])
@handle_server_exception
def get_account_by_id(accountId: int):
    account = Account.get_account_by_id(accountId)

    if not account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    return Account.to_json(account)


@app.route('/accounts/<accountId>', methods=['PUT'])
@handle_server_exception
def update_account_by_id(accountId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('balance', type=Decimal, help='balance can not be blank', required=True)

    data = parser.parse_args()
    balance = data['balance']

    if balance > 0:
        return handle_error_format('Balance must be positive number.',
                                   'Field \'balance\' in the request body.'), 400

    account = Account.get_account_by_id(accountId)

    if not account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    account.balance = balance

    Account.save_to_db(account)

    return Account.to_json(account)


@app.route('/accounts/<accountId>', methods=['DELETE'])
@handle_server_exception
def delete_account_by_id(accountId: int):
    return Account.delete_account_by_id(accountId)


@app.route('/accounts/<fromAccountId>/transferto/<toAccountId>', methods=['POST'])
@handle_server_exception
def transfer(fromAccountId: int, toAccountId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('balance', type=Decimal, help='balance can not be blank', required=True)

    data = parser.parse_args()
    balance = data['balance']

    if balance <= 0:
        return handle_error_format('Balance must be positive number.',
                                   'Field \'balance\' in the request body.'), 400

    from_account = Account.get_account_by_id(fromAccountId)

    if not from_account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    to_account = Account.get_account_by_id(toAccountId)

    if not to_account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    if from_account.balance < balance:
        return handle_error_format('Moneyless?',
                                   'Field \'balance\' in the request body.'), 400

    from_account.balance = from_account.balance - balance
    to_account.balance = to_account.balance + balance

    Account.save_to_db(from_account)
    Account.save_to_db(to_account)

    return {
        "userId": from_account.id,
        "toUserId": to_account.id,
        "amount": balance
    }