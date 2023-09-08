import jwt
from flask import request, jsonify
from functools import wraps
from app import app


import jwt
from datetime import datetime, timedelta
from app import app

def generate_token(email):

    payload = {
        'sub': email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token



def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401


        return f(*args, **kwargs)

    return decorated


