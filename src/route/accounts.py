from src.app import app
from decimal import Decimal
from flask_restful import reqparse
from src.models import User
from src.models import Account
from src.utils.exception_wrapper import handle_error_format
from src.utils.exception_wrapper import handle_server_exception


@app.route('/account/<userId>', methods=['POST'])
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


@app.route('/account/<accountId>', methods=['GET'])
@handle_server_exception
def get_account_by_id(accountId: int):
    account = Account.get_by_id(accountId)

    if not account:
        return handle_error_format('Account with such id does not exist.',
                                   'Field \'accountId\' in path parameters.'), 404

    return Account.to_json(account)


@app.route('/user/account/<userId>', methods=['GET'])
@handle_server_exception
def get_user_accounts(userId: int):
    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    return [Account.to_json(account) for account in user.accounts]


@app.route('/account/<accountId>', methods=['PUT'])
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


@app.route('/account/<accountId>', methods=['DELETE'])
@handle_server_exception
def delete_account_by_id(accountId: int):
    return Account.delete_by_id(accountId)


@app.route('/account/<fromAccountId>/transfer-to/<toAccountId>', methods=['POST'])
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
