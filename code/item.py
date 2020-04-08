import sqlite3
from flask import Request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# resources from flask_restful allow you to create classes for API data
class Item(Resource):
    """Flask RESTful item (resource) that performs HTTP requests
    Static Attributes:
        parser (obj): Instance of the flask_restful RequestParser class. Allows for validations on
            request bodies from HTTP requests (specifically in JSON).

    Class Methods:
        find_by_name: Takes the arguement 'name' and performs a GET query on the DB to determine
            if the item is present.

        insert: Takes in an Item as an argument. Opens a stream to the DB and performs an insert
            query to add a new data piece.

        update: Takes in an Item as an argument. If the Item is not present in the DB, creates a
            new Item using the Item argument's name attribute and adds it to the DB. Otherwise, it
            updates the item in the DB that matches the provided Item argument's name attribute.
    
    Methods:
        get: Retrieves an item from the DB using the 'name' argument provided in the URL string.
            Uses the class method find_by_name to search the DB. This requires authentication

        post: Adds a new item to the DB using the 'name' argument provided in the URL string. Adds
            a 'price' key/value pair supplied by the HTTP request JSON body. Uses find_by_name to
            check for the presence of the item.

        delete: Deletes an item the DB using the 'name argument provided in the URL string. If no
            item found, responds with appropriates JSON message.

        put: Updates or created a new item to the DB using the 'name' argument provided in the URL
            string. , with
            the 'price' key/value pair supplied by the HTTP request JSON body.
    """
    parser = reqparse.RequestParser() # request body parser from flask_restful
    # data validations
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        # DB connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # query
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        # DB Connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # query
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        # DB Connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # query
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    # create fucntions for each HTTP method you will allow for the
    # resource

    # Need to receive from client Header: Authorization / "JWT token"
    # NOTE remove the "" from the JWT token in the header.
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)

        # data presence check
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # data presence check
        if Item.find_by_name(name):
            return {'messsage': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        
        # try/except block for potential DB insert failure
        try:
            Item.insert(item)
        except:
            return {'message': 'An error occured inserting the item.'}, 500 # internal server error

        return item, 201 # Http status for created

    def delete(self, name):
        # data present check
        item = Item.find_by_name(name)
        if item:
            # DB Connect
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            # query
            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query, (name,)) # single variable tuple

            connection.commit()
            connection.close()

            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        # create new item
        if item is None:
            # try/except block for potential DB insert failure
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'An error has occurred inserting the item.'}, 500 # internal server error
        # update item
        else:
            # try/except block for potential DB insert failure
            try:
                Item.update(updated_item)
            except:
                return {'message': 'An error has occurred updating the item.'}, 500 # internal server error
        return updated_item


class ItemList(Resource):
    def get(self):
        return {'items': items}