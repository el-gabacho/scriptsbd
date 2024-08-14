from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            s = Serializer(SECRET_KEY)
            data = s.loads(token)
        except SignatureExpired:
            return jsonify({'message': 'Token has expired!'}), 401
        except BadSignature:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated