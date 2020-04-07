from flask import Flask, request
from flask_restful import Resource, Api

# ==== Server =====
app = Flask(__name__)
api = Api(app)

# ==== Data =====
items = []


# ===== Resources =====
# resources from flask_restful allow you to create classes for API data
# flask_restful automatically jsonifies dictionaries
class Item(Resource):
    # create fucntions for each HTTP method you will allow for the
    # resource
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


class ItemList(Resource):
    def get(self):
        return {'items': items}


# ===== Endpoints =====
# add the class, along with the URL
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/cheese
api.add_resource(ItemList, '/items') # http//127.0.0.1:5000/items

# ===== Server =====
app.run(port=5000, debug=True)