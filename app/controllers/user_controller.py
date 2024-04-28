from flask import Blueprint, request, jsonify, session

from app.extensions import db
from app.models import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Set user_id in session here:
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'username': username}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


def get_user_id_from_session_or_token():
    return session.get('user_id')
