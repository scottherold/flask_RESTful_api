from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identify
from user import UserRegister
from item import Item, ItemList

# ==== Server =====
app = Flask(__name__)
app.secret_key = 'thisisasecretkey' # NOTE change for production
api = Api(app)

# === Security ===
jwt = JWT(app, authenticate, identify) # creates /auth endpoint

# ===== Endpoints =====
# add the class, along with the URL
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/cheese
api.add_resource(ItemList, '/items') # http//127.0.0.1:5000/items
api.add_resource(UserRegister, '/register') # http://127.0.0.1:5000/register

# ===== Server =====
# only runs if this file is the entry point for the application. This 
# does not run if this file is imported
if __name__ == '__main__':
    app.run(port=5000, debug=True)