from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'data': 'this is aku'})

if __name__ == '__main__':
    app.run()