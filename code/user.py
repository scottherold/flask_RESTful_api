import sqlite3
from flask_restful import Resource, reqparse

class User:
    """A class representing the model for a User in data

    Attributes:
        id (int): The user's id in localstorage data (from security.py)
        username (str): The user's username in localstorage data (from security.py)
        password (str): The user's password in localstorage data (from secuirty.py)

    Methods:
        find_by_username: queries the sqlite DB for a user, using the 'username' argument as a 
            value for the query with parameter replacement. Returns the user object if found,
            otherwise returns None.
        find_by_id: queries the sqlite DB for a user, using the 'id' argument as a 
            value for the query with parameter replacement. Returns the user object if found,
            otherwise returns None.
    """
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # single value tuple needs a commma
        row = result.fetchone() # gets first result from query
        if row:
            user = User(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,)) # single value tuple needs a commma
        row = result.fetchone() # gets first result from query
        if row:
            user = User(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    """A class that extends the flask_restful Resource class. Allows the user to register for 
    access
    
    Static Attributes:
        parser (obj): Instance of the flask_restful RequestParser class. Allows for validations on
            request bodies from HTTP requests (specifically in JSON)

    Methods:
        post: Creates a new user. Uses the JSON data in the HTTP request body, along with the
            parser static attribute to validate that username and password data are present. If so,
            the new user is added to the sqlite DB, otherwise the validation errors are returned.
    """

    # Request body parser
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'Username cannot be left blank!'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'Password cannot be left blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        # Duplicate username check
        if User.find_by_username(data['username']):
            return {"message": "Username exists, please choose a different username."}, 400

        # DB Connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)" # id field MUST be null to auto-increment
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201