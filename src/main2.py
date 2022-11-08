#!/usr/bin/env python3

import uuid, os, hashlib, json
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort
from time import ctime

app = Flask(__name__)
api = Api(app)

''' Global variables '''
__version__ = 'v0.0.1-alpha'
USERS_PATH = "users/"
tokens_dict = {}

''' Global functions '''
def generate_access_token():
    ''' Generate random token for a new user '''
    return str(uuid.UUID(bytes=os.urandom(16), version=4))

def encrypt_password(salt, password):
    ''' Encrypt password using SHA256 algorithm'''
    return hashlib.sha256(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()

def check_authorization_header(user_id):
    ''' Check if token is correct '''
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]
        
    if user_id in tokens_dict:
        if (tokens_dict[user_id] == token):
            return True
        
    return False


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
        shadow_file = open('.shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()
        
        for line in lines:
            credentials = line.split(":")
            #print("Pass: ",credentials[2])
            #print("Trying: ",encrypt_password(credentials[1].strip(),password))
            if (credentials[0] == username and credentials[2].strip() == encrypt_password(credentials[1],password)):
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
        if not os.path.isdir(USERS_PATH + username):
            os.system("mkdir " + USERS_PATH + username)

    def register_user(self, username, password):
        ''' Register new user in shadow file '''
        
        shadow_file = open('.shadow', 'a')
        credentials = ""
        time = str(ctime())
        salt = time.replace(':','/')
        
        if (os.stat(".shadow").st_size != 0):
            credentials = "\n"

        credentials += username + ":" + salt + ":" + encrypt_password(salt,password)
        shadow_file.writelines(credentials)
        shadow_file.close()

    ''' Check if username already exists '''
    def check_username(self, username):

        if not os.path.exists('.shadow'):
            print("Creating shadow file...")
            os.system("touch .shadow")
        
        shadow_file = open('.shadow', 'r')
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

    def get(self, user_id, doc_id):
        ''' Process GET request '''
        
        if check_authorization_header(user_id):
            if os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(401, message="The file does not exist")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                with open(json_file_name) as json_file:
                    data = json.load(json_file) 

                return data
        else:
            abort(401, message="Token is not correct")
    
    def post(self, user_id, doc_id):
        ''' Process POST request '''
        if (check_authorization_header(user_id)):
            if os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(401, message="The file already exists, use put to update")
            else:
                json_data = request.get_json(force=True)
                doc_content = json_data['doc_content']
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"

                json_string = json.dumps(doc_content)
                with open(json_file_name, 'w') as outfile:
                    outfile.write(json_string)

                file_size = os.stat(json_file_name)

                return jsonify(size=file_size.st_size)
        else:
            abort(401, message="Token is not correct")
    
    def put(self, user_id, doc_id):
        ''' Process PUT request '''

        if (check_authorization_header(user_id)):
            # Delete json file
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(401, message="The file does not exists, use post to create")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                os.remove(json_file_name)
                    
                # Create new json file
                json_data = request.get_json(force=True)
                doc_content = json_data['doc_content']

                json_string = json.dumps(doc_content)
                with open(json_file_name, 'w') as outfile:
                    outfile.write(json_string)

                file_size = os.stat(json_file_name)

                return jsonify(size=file_size.st_size)
        else:
            abort(401, message="Token is not correct")
    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''

        if (check_authorization_header(user_id)):
            if os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(401, message="The file does not exits")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                os.remove(json_file_name)
                return "{}"
        else:
            abort(401, message="Token is not correct")

class AllDocs(Resource):

    def get(self, user_id):
        
        if (check_authorization_header(user_id)):
            all_docks = {}
            path = os.listdir(USERS_PATH + user_id)
            for files in path:
                    with open(USERS_PATH + user_id+"/"+files) as content:
                        all_docks[files] = json.load(content)
            return jsonify(all_docks)
        else :
            abort(401, message="Token is not correct")


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
