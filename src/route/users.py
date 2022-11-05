from src.app import app
from src.models import User
from flask_restful import reqparse
from src.utils.exception_wrapper import handle_error_format
from src.utils.exception_wrapper import handle_server_exception


@app.route('/user/create', methods=['POST'])
@handle_server_exception
def create_user():
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank', required=True)
    parser.add_argument('firstName', help='firstName cannot be blank', required=True)
    parser.add_argument('lastName', help='lastName cannot be blank', required=True)
    parser.add_argument('email', help='email cannot be blank', required=True)
    parser.add_argument('password', help='password cannot be blank', required=True)

    data = parser.parse_args()
    username = data['username']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    password = data['password']
    password_hash = User.generate_hash(password)

    if '@' not in email:
        return handle_error_format('Please, enter valid email address.', 'Field \'email\' in the request body.'), 400

    if len(password) < 8:
        return handle_error_format('Password should consist of at least 8 symbols.',
                                   'Field \'password\' in the request body.'), 400

    if User.get_by_username(username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash
    )
    new_user.save_to_db()

    return User.to_json(new_user)


@app.route('/user/<userId>', methods=['GET'])
@handle_server_exception
def get_user_by_id(userId: int):
    user = User.get_by_id(userId)
    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404
    return User.to_json(user)


@app.route('/user/<userId>', methods=['PUT'])
@handle_server_exception
def update_user_by_id(userId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank')
    parser.add_argument('firstName', help='firstName cannot be blank')
    parser.add_argument('lastName', help='lastName cannot be blank')

    data = parser.parse_args()
    username = data['username']
    first_name = data['firstName']
    last_name = data['lastName']

    if User.get_by_username(username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.save_to_db()

    return User.to_json(user)


@app.route('/user/<userId>', methods=['DELETE'])
@handle_server_exception
def delete_user_by_id(userId: int):
    return User.delete_by_id(userId)
