from flask import Flask, jsonify, session, request
from flask_cors import CORS

app = Flask(__name__)

app.config['SECRET_KEY'] = 'slkdfjsSDFSDFSDKFLLNNU'
CORS(app, supports_credentials=True)
# CORS(app, supports_credentials=True, origins=['http://localhost:3001'])

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
    f = open('./tmp/demo.txt', 'w')
    f.write(input)
    f.close()
    
    return {'msg': input + ' is written'}

@app.route('/add', methods=['POST'])
def add():
    data = request.json.get('data')

    f = open('./tmp/demo.txt', 'a')
    f.write('\n'+ data)
    f.close()

    f = open('./tmp/demo.txt', 'r')
    lines = f.readlines()
    s = '\n'.join(lines)
    return {'code': 200, 'msg': 'berhasil tambah', 'data': s}

if __name__ == '__main__':
    app.run(debug=True)