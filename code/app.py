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
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404 # sends 404 error

    def post(self, name):
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
app.run(port=5000)