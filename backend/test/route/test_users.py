from src.models import Role, User
from unittest import TestCase, mock
from undecorated import undecorated
from src.route import create_user, get_user_by_id, get_authorized_user, update_user_by_id, update_authorized_user, \
    delete_user_by_id, delete_authorized_user


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            first_name='first_name',
            last_name='last_name',
            email='email',
            password='password'
        )

        self.user_json_create = {
            'username': 'denshykk',
            'firstName': 'Denys',
            'lastName': 'Tykhonov',
            'email': 'denshykk@gmail.com',
            'password': 'whocares'
        }

        self.get_user_json = {
            'accountIds': [],
            'email': 'email',
            'first_name': 'first_name',
            'id': None,
            'last_name': 'last_name',
            'password': 'password',
            'roles': [],
            'username': 'username'
        }

        self.update_user_json = {
            'username': 'new',
            'firstName': 'new',
            'lastName': 'new'
        }

    @mock.patch('src.models.user.User.save_to_db')
    @mock.patch('src.models.role.Role.get_by_name')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('src.models.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user(self, mock_request_parser, mock_generate_hash, mock_get_by_username, mock_get_by_name,
                         mock_save_to_db):
        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'
        mock_get_by_username.return_value = False
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_save_to_db.return_value = True

        result = create_user()

        self.assertEqual({
            'accountIds': [],
            'email': 'denshykk@gmail.com',
            'first_name': 'Denys',
            'id': None,
            'last_name': 'Tykhonov',
            'password': 'password',
            'roles': [
                'user'
            ],
            'username': 'denshykk'
        }, result)

    @mock.patch('src.models.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_email_check_fail(self, mock_request_parser, mock_generate_hash):
        self.user_json_create['email'] = 'invalid'

        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'Please, enter valid email address.',
                                       'source': 'Field \'email\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_password_check_fail(self, mock_request_parser, mock_generate_hash):
        self.user_json_create['password'] = 'pass'

        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'Password should consist of at least 8 symbols.',
                                       'source': 'Field \'password\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('src.models.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_username_check_fail(self, mock_request_parser, mock_generate_hash, mock_get_by_username):
        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'
        mock_get_by_username.return_value = True

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'User with such username already exists.',
                                       'source': 'Field \'username\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.user.User.get_by_id')
    def test_get_user_by_id(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = self.user

        undecorated_get_user_by_id = undecorated(get_user_by_id)
        result = undecorated_get_user_by_id(1)

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.models.user.User.get_by_id')
    def test_get_user_by_id_with_validation_error(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None

        undecorated_get_user_by_id = undecorated(get_user_by_id)
        result = undecorated_get_user_by_id(1)

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_get_authorized_user(self, mock_current_user, mock_get_by_username):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user

        undecorated_get_authorized_user = undecorated(get_authorized_user)
        result = undecorated_get_authorized_user()

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_get_authorized_user_with_invalid_user(self, mock_current_user, mock_get_by_username):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = None

        undecorated_get_authorized_user = undecorated(get_authorized_user)
        result = undecorated_get_authorized_user()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.user.User.save_to_db')
    @mock.patch('src.models.user.User.get_by_id')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_user_by_id(self, mock_request_parser, mock_get_by_username, mock_get_by_id, mock_save_to_db):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.return_value = None
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_update_user_by_id = undecorated(update_user_by_id)
        result = undecorated_update_user_by_id(1)

        self.get_user_json['username'], self.get_user_json['first_name'], self.get_user_json[
            'last_name'] = 'new', 'new', 'new'

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_user_by_id_with_invalid_id(self, mock_request_parser, mock_get_by_username):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.return_value = self.user

        undecorated_update_user_by_id = undecorated(update_user_by_id)
        result = undecorated_update_user_by_id(1)

        self.assertEqual(({'errors': [{'message': 'User with such username already exists.',
                                       'source': 'Field \'username\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.models.user.User.get_by_id')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_user_by_id_with_invalid_username(self, mock_request_parser, mock_get_by_username, mock_get_by_id):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.return_value = None
        mock_get_by_id.return_value = None

        undecorated_update_user_by_id = undecorated(update_user_by_id)
        result = undecorated_update_user_by_id(1)

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.user.User.save_to_db')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_authorized_user(self, mock_request_parser, mock_get_by_username, mock_current_user,
                                    mock_save_to_db):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.side_effect = [None, self.user]
        mock_current_user.return_value = 'username'
        mock_save_to_db.return_value = True

        undecorated_update_authorized_user = undecorated(update_authorized_user)
        result = undecorated_update_authorized_user()

        self.get_user_json['username'], self.get_user_json['first_name'], self.get_user_json[
            'last_name'] = 'new', 'new', 'new'

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_authorized_user_with_invalid_username(self, mock_request_parser, mock_get_by_username):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.return_value = self.user

        undecorated_update_authorized_user = undecorated(update_authorized_user)
        result = undecorated_update_authorized_user()

        self.assertEqual(({'errors': [{'message': 'User with such username already exists.',
                                       'source': 'Field \'username\' in the request body.'}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_authorized_user_with_invalid_user(self, mock_request_parser, mock_get_by_username,
                                                      mock_current_user):
        mock_request_parser.return_value = self.update_user_json
        mock_get_by_username.side_effect = [None, None]
        mock_current_user.return_value = 'username'

        undecorated_update_authorized_user = undecorated(update_authorized_user)
        result = undecorated_update_authorized_user()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': 'Field \'userId\' in path parameters.'}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.user.User.delete_by_identifier')
    def test_delete_user_by_id(self, mock_delete_by_identifier):
        mock_delete_by_identifier.return_value = self.get_user_json

        undecorated_delete_user_by_id = undecorated(delete_user_by_id)
        result = undecorated_delete_user_by_id(1)

        self.assertEqual(self.get_user_json, result)

    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('src.models.user.User.delete_by_identifier')
    def test_delete_authorized_user(self, mock_delete_by_identifier, mock_current_username):
        mock_delete_by_identifier.return_value = self.get_user_json
        mock_current_username.return_value = 'username'

        undecorated_delete_authorized_user = undecorated(delete_authorized_user)
        result = undecorated_delete_authorized_user()

        self.assertEqual(self.get_user_json, result)
