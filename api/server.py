import flask
from flask import request, jsonify
from firebase import firebase
from download_sticker import StickerDownloader
from match_stats import searchWaifus
from flask_caching import Cache

#from PIL import Image
#from io import BytesIO
#import base64

app = flask.Flask(__name__)
app.config["DEBUG"] = True


cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

firebase = firebase.FirebaseApplication('https://waifu-bot-api-default-rtdb.europe-west1.firebasedatabase.app/', None)

@cache.memoize(5000)
def getAllStats():
    return firebase.get('/stats', None)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

@app.route('/api/v1/stats', methods=['GET'])
@cache.cached(timeout=5000)
def stats():
    result = getAllStats()
    return jsonify(result)

@app.route('/api/v1/stickers/<deck>', methods=['GET'])
@cache.cached(timeout=5000)
def stickers(deck):
    #result = firebase.get('/stats', None)
    #return jsonify(result)
    downloader = StickerDownloader()
    stickers = downloader.get_sticker_set(deck)
    stats = getAllStats()

    result = searchWaifus(stickers, stats)
    return jsonify(result)
    
    #im = Image.open(BytesIO(base64.b64decode(stickers[0]["data"])))
    #im.show()
    #return "<h1>Hello</h1>"

app.run()
