import jwt
from flask import jsonify, request
import app
from functools import wraps


def admin_login_required(func):
    import models
    
    @wraps(func)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return 'Token not found', 401

        if " " in token:
            token = token.split(" ")[1]

        try:
            payload = jwt.decode(token, app.app.config.get('SECRET_KEY'),
                                 algorithms='HS256')
            user_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 401
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', 401

        user = models.User.query.filter_by(id=user_id).first()

        if not user.is_admin:
            return 'You are not allowed to call this API', 403

        return func(*args, **kwargs)

    return wrap