from os import abort
import flask
from flask import request, jsonify, abort
from firebase import firebase
from download_sticker import StickerDownloader
from match_stats import matchStats
from flask_caching import Cache
from decouple import config
from flask_swagger_ui import get_swaggerui_blueprint

#from PIL import Image
#from io import BytesIO
#import base64
app = flask.Flask(__name__)
#app.config["DEBUG"] = True

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Waifu Deck API - made by fans"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
firebase = firebase.FirebaseApplication('https://waifu-bot-api-default-rtdb.europe-west1.firebasedatabase.app/', None)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400

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
    downloader = StickerDownloader(config('TELEGRAM_TOKEN'))
    stickers = downloader.get_sticker_set(deck)

    if stickers is None:
        abort(400, description="Not a valid deck")

    return jsonify(stickers)

@app.route('/api/v1/waifus/stats/get', methods=['POST'])
@cache.cached(timeout=5000)
def match():
    waifu = request.json["waifu"]
    stats = getAllStats()
    
    result = matchStats(waifu, stats)
    return jsonify(result)

