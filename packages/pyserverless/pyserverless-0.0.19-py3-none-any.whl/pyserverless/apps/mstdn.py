#!/usr/bin/env python
import base64
import os
from typing import List
from urllib.parse import quote_plus

import codefast as cf
import requests

from pyserverless.apps.rabbitmq import Consumer
from pyserverless.auth import auth

MASTODON_HOST = 'https://mstdn.social/'


class MstdnSocial(object):

    def __init__(self) -> None:
        pass

    def upload_media(self, media: List[str]) -> List[str]:
        media_ids = []
        for f in media:
            with open(f, 'rb') as fp:
                files = {'file': fp}
                r = requests.post(
                    MASTODON_HOST + 'api/v1/media',
                    files=files,
                    headers={'Authorization': 'Bearer ' + auth.mastodon_token})
                media_ids.append(r.json()['id'])
        return media_ids

    def post(self, status: str, media: List[str]) -> None:
        if media:
            media_ids = self.upload_media(media)
            cf.info(['uploaded media', media_ids])
            payload = {
                'status': status,
                'media_ids[]': media_ids,
            }
        else:
            payload = {
                'status': status,
            }
        cf.info(payload)
        r = requests.post(
            MASTODON_HOST + 'api/v1/statuses',
            data=payload,
            headers={'Authorization': 'Bearer ' + auth.mastodon_token})
        response = {'uri': r.json()['uri']}
        cf.info(response)
        return True


class Const(object):
    bark = type(
        'bark', (object, ), {
            'host': f'{auth.bark}/1Message/',
            'icon': 'https://s3.bmp.ovh/imgs/2022/09/24/8a33b2e0db90749d.png'
        })

    ONCE_MESSAGE_SET = 'ONCE_MESSAGE_SET_2023'


class Channel(object):

    @staticmethod
    def post(content: str) -> bool:
        cf.info(['posting message ', content])
        url = Const.bark.host + quote_plus(content)
        url += '?icon=' + Const.bark.icon
        cf.net.get(url)


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
        MstdnSocial().post(text, medias)
        Channel.post('MSTDN POSTED SUCCESSFULLY')
        return {'status': 'success'}
    except Exception as e:
        cf.error('error when post tweet {}'.format(e))
        return {'status': 'failed', 'message': str(e)}
