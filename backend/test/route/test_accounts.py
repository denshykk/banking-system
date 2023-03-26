from unittest import TestCase, mock
from undecorated import undecorated
from src.models import User, Account, Role
from src.route import create_account, create_account_for_authorized_user, get_account_by_id, get_user_accounts, \
    get_authorized_user_accounts, update_account_by_id, delete_account_by_id, transfer_to_account


class TestAccounts(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            first_name='first_name',
            last_name='last_name',
            email='email',
            password='password'
        )

        self.account = Account(
            balance=0,
            userId=1
        )

        self.account2 = Account(
            balance=0,
            userId=2
        )

        self.user_role = Role(
            id=1,
            name='user'
        )

        self.admin_role = Role(
            id=2,
            name='admin'
        )

        self.user.accounts.append(self.account)
        self.user.roles.append(self.user_role)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.user.User.get_by_id')
    def test_create_account(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_create_account = undecorated(create_account)
        result = undecorated_create_account(1)

        self.assertEqual({'balance': 0, 'id': None, 'user_id': 1}, result)

    @mock.patch('src.models.user.User.get_by_id')
    def test_create_account_with_invalid_user(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        undecorated_create_account = undecorated(create_account)
        result = undecorated_create_account(1)

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_create_account_for_authorized_user(self, mock_current_user, mock_get_by_username, mock_save_to_db):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_create_account_for_authorized_user = undecorated(create_account_for_authorized_user)
        result = undecorated_create_account_for_authorized_user()

        self.assertEqual({'balance': 0, 'id': None, 'user_id': None}, result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_create_account_for_authorized_user_with_invalid_user(self, mock_current_user, mock_get_by_username):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = None

        undecorated_create_account_for_authorized_user = undecorated(create_account_for_authorized_user)
        result = undecorated_create_account_for_authorized_user()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Account.get_by_id')
    def test_get_account_by_id(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.account
        mock_save_to_db.return_value = True

        undecorated_get_account_by_id = undecorated(get_account_by_id)
        result = undecorated_get_account_by_id(1)

        self.assertEqual({'balance': 0, 'id': None, 'user_id': 1}, result)

    @mock.patch('src.models.Account.get_by_id')
    def test_get_account_by_id_with_invalid_account_id(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        undecorated_get_account_by_id = undecorated(get_account_by_id)
        result = undecorated_get_account_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Account with such id does not exist.',
                                       'source': 'Field \'accountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.User.get_by_id')
    def test_get_user_accounts(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_get_user_accounts = undecorated(get_user_accounts)
        result = undecorated_get_user_accounts(1)

        self.assertEqual([{'balance': 0, 'id': None, 'user_id': 1}], result)

    @mock.patch('src.models.User.get_by_id')
    def test_get_user_accounts_with_invalid_user(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        undecorated_get_user_accounts = undecorated(get_user_accounts)
        result = undecorated_get_user_accounts(1)

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_get_authorized_user_accounts(self, mock_current_user, mock_get_by_username, mock_save_to_db):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_get_authorized_user_accounts = undecorated(get_authorized_user_accounts)
        result = undecorated_get_authorized_user_accounts()

        self.assertEqual([{'balance': 0, 'id': None, 'user_id': 1}], result)

    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_get_authorized_user_accounts_with_invalid_user(self, mock_current_user, mock_get_by_username):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = None

        undecorated_get_authorized_user_accounts = undecorated(get_authorized_user_accounts)
        result = undecorated_get_authorized_user_accounts()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.user.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_account_by_id(self, mock_request_parser, mock_get_by_id, mock_save_to_db):
        mock_request_parser.return_value = {'balance': 2453.32}
        mock_get_by_id.return_value = self.account
        mock_save_to_db.return_value = True

        undecorated_update_account_by_id = undecorated(update_account_by_id)
        result = undecorated_update_account_by_id(1)

        self.assertEqual({'balance': 2453.32, 'id': None, 'user_id': 1}, result)

    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_account_by_id_with_invalid_balance(self, mock_request_parser):
        mock_request_parser.return_value = {'balance': -1.23}

        undecorated_update_account_by_id = undecorated(update_account_by_id)
        result = undecorated_update_account_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Balance must be positive number.',
                                       'source': 'Field \'balance\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.user.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_account_by_id_with_invalid_account(self, mock_request_parser, mock_get_by_id):
        mock_request_parser.return_value = {'balance': 2453.32}
        mock_get_by_id.return_value = None

        undecorated_update_account_by_id = undecorated(update_account_by_id)
        result = undecorated_update_account_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Account with such id does not exist.',
                                       'source': 'Field \'accountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.delete_by_id')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_delete_account_by_id(self, mock_current_user, mock_get_by_username, mock_get_by_name, mock_get_by_id,
                                  mock_delete_by_id):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_delete_by_id.return_value = Account.to_json(self.account)

        undecorated_delete_account_by_id = undecorated(delete_account_by_id)
        result = undecorated_delete_account_by_id(1)

        self.assertEqual({'balance': 0, 'id': None, 'user_id': 1}, result)

    @mock.patch('src.models.Account.delete_by_id')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_delete_account_by_id_with_admin_role(self, mock_current_user, mock_get_by_username, mock_get_by_name,
                                                  mock_delete_by_id):
        self.user.roles.append(self.admin_role)

        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_delete_by_id.return_value = Account.to_json(self.account)

        undecorated_delete_account_by_id = undecorated(delete_account_by_id)
        result = undecorated_delete_account_by_id(1)

        self.assertEqual({'balance': 0, 'id': None, 'user_id': 1}, result)

    @mock.patch('src.models.Account.delete_by_id')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_delete_account_by_id_with_invalid_user(self, mock_current_user, mock_get_by_username, mock_get_by_name,
                                                    mock_get_by_id,
                                                    mock_delete_by_id):
        self.user.accounts = []

        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_delete_by_id.return_value = Account.to_json(self.account)

        undecorated_delete_account_by_id = undecorated(delete_account_by_id)
        result = undecorated_delete_account_by_id(1)

        self.assertEqual(({'errors': [{'message': 'You do not have account with that id',
                                       'source': 'Field \'accountId\' in path parameters'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account(self, mock_request_parser, mock_get_by_id, mock_current_user, mock_get_by_username,
                                 mock_get_by_name, mock_save_to_db):
        self.account.balance = 10000.00

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.side_effect = [self.account, self.account2]
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_save_to_db.side_effect = [Account.to_json(self.account), Account.to_json(self.account2)]

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual({'amount': 1000.32, 'toUserId': None, 'userId': None}, result)
        self.assertEqual(self.account.balance, 8999.68)
        self.assertEqual(self.account2.balance, 1000.32)

    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_with_invalid_amount(self, mock_request_parser):
        self.account.balance = 10000.00

        mock_request_parser.return_value = {'amount': -1.00}

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual(({'errors': [{'message': 'Balance must be positive number.',
                                       'source': 'Field \'amount\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_with_invalid_from_user(self, mock_request_parser, mock_get_by_id):
        self.account.balance = 10000.00

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.return_value = None

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual(({'errors': [{'message': 'Account with such id does not exist.',
                                       'source': 'Field \'accountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_with_admin_role(self, mock_request_parser, mock_get_by_id, mock_current_user,
                                                 mock_get_by_username, mock_get_by_name, mock_save_to_db):
        self.account2.balance = 10000.00
        self.user.roles.append(self.admin_role)

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.side_effect = [self.account2, self.account]
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_save_to_db.side_effect = [Account.to_json(self.account), Account.to_json(self.account2)]

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual({'amount': 1000.32, 'toUserId': None, 'userId': None}, result)
        self.assertEqual(self.account.balance, 1000.32)
        self.assertEqual(self.account2.balance, 8999.68)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_without_account_perms_and_admin_role(self, mock_request_parser, mock_get_by_id,
                                                                      mock_current_user, mock_get_by_username,
                                                                      mock_get_by_name, mock_save_to_db):
        self.account2.balance = 10000.00

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.side_effect = [self.account2, self.account]
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_save_to_db.side_effect = [Account.to_json(self.account), Account.to_json(self.account2)]

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual(({'errors': [{'message': 'You do not have access to this account.',
                                       'source': 'Field \'fromAccountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_with_invalid_to_account(self, mock_request_parser, mock_get_by_id, mock_current_user,
                                                         mock_get_by_username, mock_get_by_name, mock_save_to_db):
        self.account.balance = 10000.00

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.side_effect = [self.account, None]
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_save_to_db.side_effect = [Account.to_json(self.account), Account.to_json(self.account2)]

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual(({'errors': [{'message': 'Account with such id does not exist.',
                                       'source': 'Field \'accountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Account.save_to_db')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.Account.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_transfer_to_account_with_invalid_balance(self, mock_request_parser, mock_get_by_id, mock_current_user,
                                                      mock_get_by_username, mock_get_by_name, mock_save_to_db):
        self.account.balance = 500.00

        mock_request_parser.return_value = {'amount': 1000.32}
        mock_get_by_id.side_effect = [self.account, self.account2]
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.account
        mock_save_to_db.side_effect = [Account.to_json(self.account), Account.to_json(self.account2)]

        undecorated_transfer_to_account = undecorated(transfer_to_account)
        result = undecorated_transfer_to_account(1, 2)

        self.assertEqual(({'errors': [{'message': 'Moneyless?',
                                       'source': 'Field \'amount\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)
