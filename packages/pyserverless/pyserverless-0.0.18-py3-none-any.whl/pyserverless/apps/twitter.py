import base64
import os
from typing import List
from urllib.parse import quote_plus

import codefast as cf
import twitter

from pyserverless.auth import auth


class Const(object):
    bark = type(
        'bark',
        (object, ),
        {
            'host': 'https://api.day.app/3n8bS6J5MWJPVKXvkfUGRY/1Message/',
            'icon':
            'https://s3.bmp.ovh/imgs/2022/09/24/8a33b2e0db90749d.png'     # twitter logo
        })

    ONCE_MESSAGE_SET = 'ONCE_MESSAGE_SET_2022'
    task_dict = cf.mydb('/tmp/twitter.db')


class Channel(object):

    @staticmethod
    def post(content: str) -> bool:
        cf.info(['posting message ', content])
        url = Const.bark.host + quote_plus(content)
        url += '?icon=' + Const.bark.icon
        cf.net.get(url)


class Twitter(twitter.Api):

    def __init__(self, consumer_key, consumer_secret, access_token_key,
                 access_token_secret):
        super(Twitter, self).__init__(consumer_key, consumer_secret,
                                      access_token_key, access_token_secret)

    def hi(self):
        print('Hi, Twitter.')

    def get_blocks(self):
        return self.GetBlocks(skip_status=True)

    def block_by_screenname(self, screen_name):
        self.CreateBlock(screen_name=screen_name)

    def post_status(self, text: str, media=[]):
        resp = self.PostUpdate(text, media=media)
        print("Text  : {}\nMedia : {}\nResponse:".format(text, media))
        cf.info(resp)

    def post(self, args: list):
        ''' post_status wrapper'''
        assert isinstance(args, list)

        text, media = '', []
        media_types = ('.png', '.jpeg', '.jpg', '.mp4', '.gif')

        for e in args:
            if cf.io.exists(e):
                if e.endswith(media_types):
                    media.append(e)
                else:
                    text += cf.io.read(e, '')
            else:
                text += e
        self.post_status(text, media)


class TweetServer(object):

    def __init__(self):
        keys = auth.twitter_api
        self.twitter_api = Twitter(keys['consumer_key'],
                                   keys['consumer_secret'],
                                   keys['access_token'],
                                   keys['access_token_secret'])

    def post(self, text: str, images: List[str]):
        """ Parse out tweet text and image, and then post them
        msg demo:
        {
            'text':'hello world',
            'images':['m1':'some binary string', 'm2':'some binary string']
        }
        """
        try:
            medias = []
            for name, content in images:
                _path = os.path.join('/tmp', name)
                medias.append(_path)
                with open(_path, 'wb') as f:
                    cf.info(['writing to ', _path])
                    f.write(base64.b64decode(content))
            self.twitter_api.post([text] + medias)
            Channel.post('TWEET POSTED SUCCESSFULLY')
        except Exception as e:
            cf.error('error when post tweet {}'.format(e))


def post_status(text: str, images: List[str]) -> dict:
    """ Parse out tweet text and image, and then post them
    msg demo:
    {
        'text':'hello world',
        'images':['m1':'some binary string', 'm2':'some binary string']
    }
    """
    try:
        medias = []
        for name, content in images:
            _path = os.path.join('/tmp', name)
            medias.append(_path)
            with open(_path, 'wb') as f:
                cf.info(['writing to ', _path])
                f.write(base64.b64decode(content))
        TweetServer().post(text, medias)
        Channel.post('TWEET POSTED SUCCESSFULLY')
        return {'status': 'success'}
    except Exception as e:
        cf.error('error when post tweet {}'.format(e))
        return {'status': 'failed', 'message': str(e)}
