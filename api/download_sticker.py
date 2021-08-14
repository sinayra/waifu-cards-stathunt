import requests
import json
import urllib.parse
import time
import os
import base64
from concurrent.futures import as_completed, ThreadPoolExecutor


class File:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return '<F:{}>'.format(self.name)

class StickerDownloader:
    def __init__(self, token, session=None, multithreading=4):
        self.THREADS = multithreading
        self.token = token
        self.cwd = os.getcwd()
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        self.api = 'https://api.telegram.org/bot{}/'.format(self.token)
        verify = self._api_request('getMe', {})
        if verify['ok']:
            pass
        else:
            print('Invalid token.')
            #exit()

    def _api_request(self, fstring, params):
        try:
            param_string = '?' + urllib.parse.urlencode(params)
            res = self.session.get('{}{}{}'.format(self.api, fstring, param_string))
            if res.status_code != 200:
                raise Exception
            res = json.loads(res.content.decode('utf-8'))
            if not res['ok']:
                raise Exception(res['description'])
            return res

        except Exception as e:
            print('API method {} failed. Error: "{}"'.format(fstring, e))
            return None

    def get_file(self, file_id):
        info = self._api_request('getFile', {'file_id': file_id})
        f = File(name=info['result']['file_path'].split('/')[-1],
                 link='https://api.telegram.org/file/bot{}/{}'.format(self.token, info['result']['file_path']))

        return f

    def get_sticker_set(self, name):
        """
        Get a list of File objects.
        :param name:
        :return:
        """
        params = {'name': name}
        if ("_by_WaifuCardsBot" not in name):
            return None

        res = self._api_request('getStickerSet', params)
        if res is None:
            return None
        stickers = res['result']['stickers']
        files = []
        #print('Starting to scrape "{}" ..'.format(name))
        #start = time.time()
        stickers_blobs = []

        #for i in stickers:
        #    file = await self.get_file(i['file_id'])
        #    files.append(file)

        with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
            futures = [executor.submit(self.get_file, i['file_id']) for i in stickers]
            for i in as_completed(futures):
                files.append(i.result())

        #end = time.time()
        #print('Time taken to scrape {} stickers - {:.3f}s'.format(len(files), end - start))
        #print()

        sticker_set = {
            'name': res['result']['name'].lower(),
            'title': res['result']['title'],
            'files': files
        }

        for f in sticker_set['files']:
            res = self.session.get(f.link)

            stickers_blobs.append(base64.b64encode(res.content).decode("utf-8"))

        return stickers_blobs

