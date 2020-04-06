from flask import Flask
from flask_restful import Resource, Api

# ==== Server =====
app = Flask(__name__)
api = Api(app)


# ===== Resources =====
# resources from flask_restful allow you to create classes for API data
class Student(Resource):
    # create fucntions for each HTTP method you will allow for the
    # resource
    def get(self, name):
        return {'student': name}


# ===== Endpoints =====
# add the class, along with the URL
api.add_resource(Student, '/student/<string:name>') # http://127.0.0.1:5000/student/Scott

# ===== Server =====
app.run(port=5000)