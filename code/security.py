from werkzeug.security import safe_str_cmp # flask library
from user import User

# ===== Mock Users DB =====
users = [
    User(1, 'bob', 'asdf')
]

username_mapping = { u.username: u for u in users } # lambda function
userid_mapping = { u.id: u for u in users } # lambda function


# ===== Security Functions =====
def authenticate(username, password):
    user = username_mapping.get(username, None)
    # safe_str_cmp is a safer method for string1 == string2
    if user and safe_str_cmp(user.password, password):
        return user

# from flask_jwt
def identify(payload):
    # Need to receive from client Header: Authorization / JWT token
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)