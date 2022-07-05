from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return {'ok': False}
    elif data['username'] == 'asimsheikh' and data['password'] == 'asim':
        return {'ok': True}
    else:
        return {'ok': False}
        # raise Exception('No idea why we are here')

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return data

@app.route('/name', methods=['POST'])
def name():
    data = request.json
    if not data:
        return {'ok': False}
    elif data['hello'] == 'world':
        return {'ok': True}

