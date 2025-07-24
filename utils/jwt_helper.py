from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in allowed_roles:
                return jsonify({"error": "Permission denied"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
