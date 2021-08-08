import flask
from flask import request, jsonify
from firebase import firebase

app = flask.Flask(__name__)
app.config["DEBUG"] = True

firebase = firebase.FirebaseApplication('https://waifu-bot-api-default-rtdb.europe-west1.firebasedatabase.app/', None)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    result = firebase.get('/stats', None)
    return jsonify(result)

app.run()
