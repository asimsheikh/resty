from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'asimsheikh' and data['password'] == 'asim':
        return {'ok': True}
    else:
        return {'ok': False}
