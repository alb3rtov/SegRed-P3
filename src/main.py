#!/usr/bin/env python3

import uuid, os, hashlib
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

''' Global variables '''
__version__ = 'v0.0.1-alpha'
tokens_dict = {}

''' Global functions '''
def generate_access_token():
    ''' Generate random token for a new user '''
    return str(uuid.UUID(bytes=os.urandom(16), version=4))

def encrypt_password(password):
    ''' Encrypt password using SHA256 algorithm'''
    return hashlib.sha256(password.encode()).hexdigest()

''' Classes '''
class Version(Resource):
    ''' Version class '''    
    def get(self):
        ''' Return software version '''
        return {'version' : __version__}

class Login(Resource):
    ''' Login class '''
    def check_credentials(self, username, password):
        ''' Check if credentials are correct '''
        shadow_file = open('shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()
        
        for line in lines:
            credentials = line.split(":")
            if (credentials[0] == username and credentials[1].strip() == encrypt_password(password)):
                return True
        
        return False

    def post(self):
        ''' Process POST request '''
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']

        if (self.check_credentials(un,pw)):
            if un in tokens_dict:
                return jsonify(access_token=tokens_dict[un])
            else:
                token = generate_access_token()
                tokens_dict[un] = token
                return jsonify(access_token=token)
        else:
            abort(401, message="Error, user or password incorrect")
            #return "Error, user or password incorrect.", 401

class SignUp(Resource):
    ''' SignUp class '''
    def create_directory(self, username):
        ''' Create directory of user if does not exists '''
        if not os.path.isdir(username):
            os.system("mkdir " + username)

    def register_user(self, username, password):
        ''' Register new user in shadow file '''
        shadow_file = open('shadow', 'a')
        credentials = ""

        if (os.stat("shadow").st_size != 0):
            credentials = "\n"

        credentials += username + ":" + encrypt_password(password)
        shadow_file.writelines(credentials)
        shadow_file.close()

    def check_username(self, username):
        ''' Check if username already exists '''
        shadow_file = open('shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()

        for line in lines:
            if (line.split(":")[0] == username):
                return True
        
        return False

    def post(self):
        ''' Process POST request '''
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']

        if (self.check_username(un)):
            #return "Error, username " + un + " already exists.", 401
            abort(401, message="Error, username {} already exists.".format(un))
        else:
            self.register_user(un, pw)
            self.create_directory(un)

            token = generate_access_token();
            tokens_dict[un] = token
            return jsonify(access_token=token)

class User(Resource):
    ''' User class '''
    def check_authorization_header(self, user_id):
        ''' Check if token is correct '''
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1]
        
        if user_id in tokens_dict:
            if (tokens_dict[user_id] == token):
                return True
        
        return False

    def get(self, user_id, doc_id):
        ''' Process GET request '''
        if (self.check_authorization_header(user_id)):
            return jsonify(user=user_id,doc=doc_id)
        else:
            abort(401, message="Token is not correct")
    
    def post(self, user_id, doc_id):
        ''' Process POST request '''
        if (self.check_authorization_header(user_id)):
            return jsonify(user=user_id,doc=doc_id)
        else:
            abort(401, message="Token is not correct")
    
    def put(self, user_id, doc_id):
        ''' Process PUT request '''
        if (self.check_authorization_header(user_id)):
            return jsonify(user=user_id,doc=doc_id)
        else:
            abort(401, message="Token is not correct")
    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''
        if (self.check_authorization_header(user_id)):
            return jsonify(user=user_id,doc=doc_id)
        else:
            abort(401, message="Token is not correct")

api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(User, '/<user_id>/<doc_id>')

if __name__ == '__main__':
    app.run(debug=True)