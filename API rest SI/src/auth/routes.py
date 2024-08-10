import os
from . import auth
from flask import request, jsonify
from models import Usuario
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    user = Usuario.query.filter_by(usuario=username).first()
    print(user)
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    token = user.generate_token(SECRET_KEY)
    return jsonify({'token': token})

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    user = Usuario.query.filter_by(usuario=username).first()
    if user is not None:
        return jsonify({'error': 'Username already exists'}), 400
    user = Usuario(usuario=username)
    user.set_password(password)
    user.save()
    return jsonify({'message': 'User created successfully'})

@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'User logged out successfully'})