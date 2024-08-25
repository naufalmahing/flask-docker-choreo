from flask import Flask, jsonify

app = Flask(__name__)

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