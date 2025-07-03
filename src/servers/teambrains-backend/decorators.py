# decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role != role:
                return jsonify({"msg": "Accès refusé : droits insuffisants"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
