import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)

from flask import Flask, jsonify, session, request
from flask_cors import CORS
import flask_cors

from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies


app = Flask(__name__)

# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(app)

app.config['SECRET_KEY'] = 'slkdfjsSDFSDFSDKFLLNNU'
CORS(app, supports_credentials=True)
# CORS(app, supports_credentials=True, origins=['http://localhost:3001'])

@app.route("/login_without_cookies", methods=["POST"])
def login_without_cookies():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)


@app.route("/login_with_cookies", methods=["POST"])
def login_with_cookies():
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity="example_user")
    set_access_cookies(response, access_token)
    return response


@app.route("/logout_with_cookies", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route("/protected", methods=["GET", "POST"])
@jwt_required()
def protected():
    return jsonify(foo="bar")

@app.route('/set-session/<username>')
def set_user(username):
    session['username'] = username
    return {'msg': 'success', 'username': username}

@app.route('/get-session')
def get_user():
    return 'hello there ' + session['username'] if session['username'] else 'there\'s no user'

@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'this is aku'})

# update flask cors root logger
# flask_cors_rootlogger = flask_cors.rootlogger
flask_cors.rootlogger.removeHandler(flask_cors.rootlogger.handlers[0])
flask_cors.rootlogger.addHandler(logging.StreamHandler(stream=sys.stdout))
flask_cors.rootlogger.setLevel(logging.DEBUG)

@app.route('/write/<input>')
def write(input):
    # try logging
    flask_cors.rootlogger.debug('domo flask cors deesu')
    print('flask cors logger handlers', flask_cors.rootlogger.handlers)
    app.logger.debug('this is flask app')

    er = None
    try:
        f = open('/tmp/demo.txt', 'w')
        f.write(input)
        f.close()
    except Exception as er:
        er = type(er)
        
    
    if er:
        return {'msg': 'Error is ' + er}
    return {'msg': input + ' is written'}

@app.route('/add', methods=['POST'])
def add():
    data = request.json.get('data')

    f = open('/tmp/demo.txt', 'a')
    f.write('\n'+ data)
    f.close()

    f = open('/tmp/demo.txt', 'r')
    lines = f.readlines()
    s = '\n'.join(lines)
    app.logger.debug('add is done no?!')
    # print(flask_cors.rootlogger.handlers)
    # flask_cors.rootlogger.removeHandler(flask_cors.rootlogger.handlers[0])
    # print(flask_cors.rootlogger.handlers)
    # flask_cors.rootlogger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # flask_cors.rootlogger.setLevel(logging.INFO)
    # flask_cors.rootlogger.debug('this is the new flask cors')
    return {'code': 200, 'msg': 'berhasil tambah', 'data': s}

# handler = logging.StreamHandler(stream=sys.stdout)
# handler.setLevel(logging.DEBUG)
# flask_cors.rootlogger.removeHandler(flask_cors.rootlogger.handlers[0])
# flask_cors.rootlogger.addHandler(handler)

if __name__ == '__main__':
    app.run(debug=True)