from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identify

# ==== Server =====
app = Flask(__name__)
app.secret_key = 'thisisasecretkey' # NOTE change for production
api = Api(app)

# === Security ===
jwt = JWT(app, authenticate, identify) # creates /auth endpoint

# ==== Data =====
items = []


# ===== Resources =====
# resources from flask_restful allow you to create classes for API data
# flask_restful automatically jsonifies dictionaries
class Item(Resource):
    """Flask RESTful item (resource) that performs HTTP requests
    
    Methods:
        get: Retrieves an item from the local data storage (items list in data) using the 'name'
            argument provided in the URL string. This requires authentication

        post: Adds a new item to local storage (items list in data) using the 'name' argument
            provided in the URL string. Adds a 'price' key/value pair supplied by the HTTP request
            JSON body.

        delete: Deletes an item in local storage (items list in data) using the 'name argument
            provided in the URL string. If no item found, responds with appropriates JSON message.

        put: Updates or created a new item to local storage (items list in data) using the 'name'
            argument provided in the URL string. If the item is not present in local storage,
            creates a new item and appends it to the localstorage items list. Otherwise, it
            updates the item in the localstorage list that matches the name argument provided, with
            the 'price' key/value pair supplied by the HTTP request JSON body.
    """
    # create fucntions for each HTTP method you will allow for the
    # resource

    # Need to receive from client Header: Authorization / "JWT token"
    # NOTE remove the "" from the JWT token in the header.
    @jwt_required()
    def get(self, name):
        # filter using lambda function
        # filter can return whatever data type you please; 'next'
        # returns a single item, but you can also use 'list' to return
        # a list.
        # NOTE: you can call 'next' multiple times for
        # additional items. 'next' can cause an error if there are no
        # items returned from the filter function, so you need to add
        # the None argument for if no items are returned
        item = next(filter(lambda x: x['name'] == name, items), None)

        # ternary if statement for if item is returned, or None (from
        # filter)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # similar lambda from get; validates that there is no item with
        # the requested name
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'messsage': "An item with name '{}' already exists".format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # Http status for created

    def delete(self, name):
        global items # sets the below items variable to the global scoped items variable
        # lambda to mutate a new list from the items list
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser() # request body parser from flask_restful
        # data validations
        parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left blank!"
        )
        data = parser.parse_args()

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


# ===== Endpoints =====
# add the class, along with the URL
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/cheese
api.add_resource(ItemList, '/items') # http//127.0.0.1:5000/items

# ===== Server =====
app.run(port=5000, debug=True)