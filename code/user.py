class User:
    """A class representing the model for a User in data

    Attributes:
        id (int): The user's id in localstorage data (from security.py)
        username (str): The user's username in localstorage data (from security.py)
        password (str): The user's password in localstorage data (from secuirty.py)
    """
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password