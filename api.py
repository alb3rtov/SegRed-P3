#!/usr/bin/env python3

import uuid, os
from flask import jsonify, Flask, request
from flask_restful import reqparse, Resource, Api

__version__ = 'v0.0.1-alpha'

app = Flask(__name__)
api = Api(app)

users = []
passwords = []
tokens = []

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Version(Resource):
    def get(self):
        return {'version' : __version__}

class Login(Resource):
    def check_credentials(self, username, password):
        try:
            user_id = users.index(username)
            pass_id = passwords.index(password)
            if (user_id == pass_id):
                return True
            else:
                return False
        except ValueError:
            return False     

    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']
        if (self.check_credentials(un,pw)):
            return jsonify(access_token=tokens[users.index(un)])
        else:
            return "Error, user or password incorrect.", 401
  
class SignUp(Resource):
    def check_username(self, username):
        if (username in users):
            return True
        else:
            return False

    def generate_access_token(self):
        return uuid.UUID(bytes=os.urandom(16), version=4)

    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']

        if (self.check_username(un)):
            return "Error, username " + un + " already exists.", 401
        else:
            users.append(un)
            passwords.append(pw)
            token = self.generate_access_token();
            tokens.append(token)
            return jsonify(access_token=token)

api.add_resource(HelloWorld, '/')
api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')

if __name__ == '__main__':
    app.run(debug=True)