import requests
import json
import urllib.parse
import time
import os
import string
import random
from PIL import Image
import asyncio

TOKEN = ''

def assure_folder_exists(folder, root):
    full_path = os.path.join(root, folder)
    if os.path.isdir(full_path):
        pass
    else:
        os.mkdir(full_path)
    return full_path


def random_filename(length, ext):
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(length)]) + '.{}'.format(ext)

def waifu_filename(index, ext):
    return ''.join("waifu") + str(index) + '.{}'.format(ext)

# TODO: Replace with a named tuple
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
            exit()

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

    async def get_file(self, file_id):
        info = self._api_request('getFile', {'file_id': file_id})
        f = File(name=info['result']['file_path'].split('/')[-1],
                 link='https://api.telegram.org/file/bot{}/{}'.format(self.token, info['result']['file_path']))

        return f

    async def get_sticker_set(self, name):
        """
        Get a list of File objects.
        :param name:
        :return:
        """
        params = {'name': name}
        res = self._api_request('getStickerSet', params)
        if res is None:
            return None
        stickers = res['result']['stickers']
        files = []
        print('Starting to scrape "{}" ..'.format(name))
        start = time.time()

        for i in stickers:
            file = await self.get_file(i['file_id'])
            files.append(file)

        #with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
        #    futures = [executor.submit(self.get_file, i['file_id']) for i in stickers]
        #    for i in as_completed(futures):
        #        files.append(i.result())

        end = time.time()
        print('Time taken to scrape {} stickers - {:.3f}s'.format(len(files), end - start))
        print()

        sticker_set = {
            'name': res['result']['name'].lower(),
            'title': res['result']['title'],
            'files': files
        }
        return sticker_set

    @staticmethod
    async def convert_file(_input, _output):
        im = Image.open(_input).convert("RGB")
        im.save(_output, "png")
        return _output

    def download_file(self, offset, link, path):
        name = ''.join('waifu') + str(offset) + '.webp'
        file_path = os.path.join(path, name)
        with open(file_path, 'wb') as f:
            res = self.session.get(link)
            f.write(res.content)

        return file_path

    async def download_sticker_set(self, sticker_set, offset):
        download_path = assure_folder_exists('waifus', root=self.cwd)
        downloads = []

        print('Starting download of "{}" into {}'.format(sticker_set['name'], download_path))
        start = time.time()

        for f in sticker_set['files']:
            filepath = self.download_file(offset, f.link, download_path)
            downloads.append(filepath)
            offset += 1

        #with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
        #    futures = [executor.submit(self.download_file, f.name, f.link, download_path) for f in sticker_set['files']]
        #    for i in as_completed(futures):
        #        downloads.append(i.result())

        end = time.time()
        print('Time taken to download {} stickers - {:.3f}s'.format(len(downloads), end - start))
        print()

        return len(downloads)
 
async def main():
    downloader = StickerDownloader(TOKEN)
    print('Welcome to Telegram Downloader..')
    urls = [
        "https://t.me/addstickers/deck_46518858_by_WaifuCardsBot",
        "https://t.me/addstickers/deck_66307063_by_WaifuCardsBot",
        "https://t.me/addstickers/deck_200822246_by_WaifuCardsBot",
        "https://t.me/addstickers/deck_213110784_by_WaifuCardsBot",
        "https://t.me/addstickers/deck_218538488_by_WaifuCardsBot",
        "https://t.me/addstickers/deck_543738428_by_WaifuCardsBot"
    ]
    names = []

    for url in urls:
        name = url.strip()
        names.append(name.split('/')[-1])

    offset = 0
    for sset in names:
        print('=' * 60)
        stickers = await downloader.get_sticker_set(sset)
        if stickers is None:
            continue
        print('-' * 60)

        offset += await downloader.download_sticker_set(stickers, offset)
        print(offset)

asyncio.run(main())
