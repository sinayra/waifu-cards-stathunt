import flask
from flask import request, jsonify
from firebase import firebase
from download_sticker import StickerDownloader
from PIL import Image
from io import BytesIO
import base64

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

@app.route('/api/v1/stickers/<deck>', methods=['GET'])
async def stickers(deck):
    #result = firebase.get('/stats', None)
    #return jsonify(result)
    downloader = StickerDownloader()
    stickers = await downloader.get_sticker_set(deck)
    
    #im = Image.open(BytesIO(base64.b64decode(stickers[0]["data"])))
    #im.show()

    return "<h1>Hello</h1>"

app.run()
