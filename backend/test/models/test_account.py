from unittest import TestCase, mock
from src.models import Account


class TestAccount(TestCase):

    def test_to_json(self):
        account = Account(id=1, balance=100, userId=1)
        expected_json = {'id': 1, 'balance': 100, 'user_id': 1}

        result = account.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        account = Account(id=1, balance=100, userId=1)

        mock_add.return_value = None
        mock_commit.return_value = None

        Account.save_to_db(account)

        mock_add.assert_called_once_with(account)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        account = Account(id=1, balance=100, userId=1)
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = account

        result = Account.get_by_id(1)

        self.assertEqual(account, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.models.account.Account.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        account = Account(id=1, balance=100, userId=1)
        mock_get_by_id.return_value = account
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Account.delete_by_id(1)

        self.assertEqual(account.to_json(), result)
        mock_get_by_id.assert_called_once_with(1)
        mock_query_property_getter.return_value.filter_by.assert_called_once_with(id=1)
        mock_query_property_getter.return_value.filter_by.return_value.delete.assert_called_once_with()
        mock_commit.assert_called_once_with()

    @mock.patch('src.models.account.Account.get_by_id')
    def test_delete_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Account.delete_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Account with such id does not exist.',
                                       'source': 'Field \'accountId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)
        mock_get_by_id.assert_called_once_with(1)
