import random
import string

from flask import request
from flask_mail import Message

from src.app import app, mail
from src.models import User
from src.utils.exception_wrapper import handle_error_format

password_reset_tokens = {}


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')

    if not User.get_by_username_or_email(email):
        return handle_error_format('User with such email does not exist.',
                                   'Field \'email\' in form params.'), 404

    token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    password_reset_tokens[token] = email

    msg = Message('Reset Your Password for Banking System', recipients=[email])
    reset_link = 'http://localhost:3000' + '/reset-password?token=' + token
    msg.body = f'Banking System.\nClick the following link to reset your password: {reset_link}'

    mail.send(msg)

    return 'An email with password reset instructions has been sent to your email address.'


@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.args.get('token')

    if token in password_reset_tokens:
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password == confirm_password:
            email = password_reset_tokens[token]
            password = User.generate_hash(new_password)

            user = User.get_by_username_or_email(email)
            user.password = password
            user.save_to_db()

            del password_reset_tokens[token]
            return 'Your password has been successfully reset.'

        return 'Passwords do not match.'

    return 'Invalid or expired token.'
