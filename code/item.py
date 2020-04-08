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
    
    Methods:
        get: Retrieves an item from the DB using the 'name' argument provided in the URL string.
            Uses the class method find_by_name to search the DB. This requires authentication

        post: Adds a new item to the DB using the 'name' argument provided in the URL string. Adds
            a 'price' key/value pair supplied by the HTTP request JSON body. Uses find_by_name to
            check for the presence of the item.

        delete: Deletes an item the DB using the 'name argument provided in the URL string. If no
            item found, responds with appropriates JSON message.

        put: Updates or created a new item to the DB using the 'name' argument provided in the URL
            string. If the item is not present in the DB, creates a new item and add it to the DB.
            Otherwise, it updates the item in the DB that matches the name argument provided, with
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
        
        # DB Connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # query
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        
        connection.commit()
        connection.close()

        return item, 201 # Http status for created

    def delete(self, name):
        global items # sets the below items variable to the global scoped items variable
        # lambda to mutate a new list from the items list
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        # create new item
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        # update item
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}