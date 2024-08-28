from flask import Flask, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

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

@app.route('/write/<input>')
def write(input):
    f = open('/tmp/demo.txt', 'w')
    f.write(input)
    f.close()
    
    return open('/tmp/demo.txt', 'r')

if __name__ == '__main__':
    app.run(debug=True)