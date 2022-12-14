#!/usr/bin/env python3

import uuid, os, hashlib, json
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort
from time import ctime
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'SegRed-P3'

''' Global variables '''
__version__ = 'v0.0.1-alpha'
USERS_PATH = "users/"
TOKENS_DICT = {}
MINUTES = 1

KEY = "195DAED626537B32D3CC7CE988ADDE5F4A000F36D13473B7D46C4E53E57F8E61"

''' Global functions '''

def verify_token(username, token):
        
        try:
            payload = jwt.decode(token, KEY, algorithms=['HS256'])
            exp = datetime.fromtimestamp(payload['exp'])

            if exp < datetime.utcnow():
                print('Token expired')
                raise jwt.ExpiredSignatureError

            if payload['username'] != username:
                print('Usuario no coincide con el token')
                raise jwt.InvalidTokenError
            
            return True
        
        except jwt.ExpiredSignatureError:
            return False
        
        except jwt.InvalidTokenError:
            return False


def check_directories():
    ''' Check if users directory and shadow file '''
    if not os.path.isdir(USERS_PATH):
        os.mkdir(USERS_PATH)
    try:
        shadow_file = open('.shadow', 'r')
        shadow_file.close()
    except FileNotFoundError:
        os.system("touch .shadow")

def generate_access_token(username):
    ''' Generate random token for a new user '''
    exp = datetime.utcnow() + timedelta(minutes=MINUTES)
    token = jwt.encode({'username': username, 'exp': exp},KEY, algorithm='HS256')
    
    return token

def encrypt_password(salt, password):
    ''' Encrypt password using SHA256 algorithm'''
    return hashlib.sha256(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()

def check_authorization_header(user_id):
    ''' Check if token is correct '''
    auth_header = request.headers.get('Authorization')
    header = auth_header.split(" ")

    if header[0] != "token":
        abort(400, message="Authorization header must be: token <user-auth-token>")

    token = header[1]
        
    if verify_token(user_id, token):
        return True

    else:
        abort(404, message="The user " + user_id + " is not registered in the system")

''' Classes '''
class Version(Resource):
    ''' Version class '''    
    def get(self):
        ''' Return software version '''
        return {'version' : __version__}

class SignUp(Resource):
    ''' SignUp class '''
    def create_directory(self, username):
        ''' Create directory of user if does not exists '''
        if not os.path.isdir(USERS_PATH + username):
            try:
                os.mkdir(USERS_PATH + username)
            except Exception:
                abort(400, message="Error creating username space")

    def register_user(self, username, password):
        ''' Register new user in shadow file '''
        shadow_file = open('.shadow', 'a')
        credentials = ""

        salt = str(uuid.uuid4())
        
        if (os.stat(".shadow").st_size != 0):
            credentials = "\n"

        credentials += username + ":" + salt + ":" + encrypt_password(salt,password)
        shadow_file.writelines(credentials)
        shadow_file.close()

    ''' Check if username already exists '''
    def check_username(self, username):

        shadow_file = open('.shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()

        for line in lines:
            if (line.split(":")[0] == username):
                return True
        
        return False

    def post(self):
        ''' Process POST request '''
        try:
            json_data = request.get_json(force=True)

            username = json_data['username']
            password = json_data['password']

        except KeyError:
            abort(400, message="Arguments must be 'username' and 'password'")
        except:
            abort(400, message="Wrong format of the file")
        else:
            if (self.check_username(username)):
                abort(409, message="Error, username {} already exists.".format(username))
            else:
                self.register_user(username, password)
                self.create_directory(username)

                token = generate_access_token(username)
                TOKENS_DICT[username] = token
                return jsonify(token)

class Login(Resource):
    ''' Login class '''
    def check_credentials(self, username, password):
        ''' Check if credentials are correct '''   
        shadow_file = open('.shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()
        
        for line in lines:
            credentials = line.split(":")
            if (credentials[0] == username and credentials[2].strip() == encrypt_password(credentials[1],password)):
                return True

        return False

    def post(self):
        ''' Process POST request '''
        try:
            json_data = request.get_json(force=True)            
            username = json_data['username']
            password = json_data['password']
        except KeyError:
            abort(400, message="Arguments must be 'username' and 'password'")
        except:
            abort(400, message="Wrong format of the file")
        else:
        #Comprobamos si el usuario esta registrado
            if (self.check_credentials(username,password)):
                #Probamos si tiene un token asociado, si no se genera
                try:
                    token = TOKENS_DICT[username]
                except KeyError:
                    token = generate_access_token(username)
                    TOKENS_DICT[username] = token
                    return jsonify(access_token=token)
                #Si lo tiene, comprobamos su fecha de caducidad, si ha expirado, los eliminamos de ambos json y generamos unos nuevos
                if verify_token(username, token):
                    return jsonify(access_token=TOKENS_DICT[username])
                else:
                    del(TOKENS_DICT[username])
                    token = generate_access_token(username)
                    TOKENS_DICT[username] = token
                    return jsonify(access_token=token)
            else:
                abort(401, message="Error, user or password incorrect")

class User(Resource):
    ''' User class '''
    def get(self, user_id, doc_id):
        ''' Process GET request ''' 
        if check_authorization_header(user_id):
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(404, message="The file does not exist")
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
                abort(405, message="The file already exists, use put to update")
            else:
                try:
                    json_data = request.get_json(force=True)
                    doc_content = json_data['doc_content']
                except KeyError:
                    abort(400, message="Argument must be 'doc_content'")
                except:
                    abort(400, message="Wrong format of the file")
                else:
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
                abort(404, message="The file does not exists")
            else:
                
                # Create new json file
                try:
                    json_data = request.get_json(force=True)
                    doc_content = json_data['doc_content']
                except:
                    abort(400, message="Wrong format of the file")
                else:
                    json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                
                    os.remove(json_file_name)
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
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(404, message="The file does not exits")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                os.remove(json_file_name)
                return "{}"
        else:
            abort(401, message="Token is not correct")

class AllDocs(Resource):
    ''' AllDocs class '''
    def get(self, user_id):
        ''' Process GET request '''
        if (check_authorization_header(user_id)):
            all_docks = {}
            path = os.listdir(USERS_PATH + user_id)
            for files in path:
                with open(USERS_PATH + user_id+"/"+files) as content:
                    all_docks[files.strip(".json")] = json.load(content)
            return jsonify(all_docks)
        else :
            abort(401, message="Token is not correct")


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')

if __name__ == '__main__':
    check_directories()
    app.run(debug=True, ssl_context=('./cert/cert.pem', './cert/key.pem'))
