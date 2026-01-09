from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt  
from flask_jwt_extended import verify_jwt_in_request

def role_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            
            verify_jwt_in_request()
            
            
            claims = get_jwt()
            
            
            if "role" not in claims or claims["role"] not in roles:
                return jsonify(msg="Access forbidden: insufficient role"), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
