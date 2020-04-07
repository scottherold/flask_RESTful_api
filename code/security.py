from werkzeug.security import safe_str_cmp # flask library
from user import User


# ===== Security Functions =====
def authenticate(username, password):
    user = User.find_by_username(username)
    # safe_str_cmp is a safer method for string1 == string2
    if user and safe_str_cmp(user.password, password):
        return user

# from flask_jwt
def identify(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)