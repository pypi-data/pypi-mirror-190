from pyserverless.bases import SingletonSession, bitly_helper
import asyncio
import hashlib
import json
import secrets
import uuid
from typing import List, Union

import aiohttp
import aioredis
import codefast as cf
from codefast.asyncio import async_render
from codefast.io.osdb import osdb
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from hashids import Hashids

from pyserverless.apps.imagehosting import github_upload
from pyserverless.apps.mstdn import post_status
from pyserverless.apps.rabbitmq import AMQPPublisher
from pyserverless.apps.twitter import post_status as tweet_status
from pyserverless.auth import auth

# ---------------------------- Bases
cf.info("Pyserverless started ...")
cache = osdb('/tmp/cache.db')

app = FastAPI()


async def get_redis():
    return await aioredis.from_url('redis://localhost')


# ---------------------------- Routes
@app.get('/hello')
async def hello_world():
    return {'hello': 'world'}


@app.post('/callback')
@app.get('/callback')
async def callback_():
    return {"code": 200, "msg": "SUCCESS", "uuid": str(uuid.uuid4())}


@app.post('/redis')
@app.get('/redis')
async def redis_(info: Request):
    info = await info.json()
    key = info.get('key')
    value = info.get('value')
    if value is None:
        return {"value": cache[key]}
    else:
        cache[key] = value
        return {"value": value, "key": key}


@app.post('/tunnels')
@app.get('/tunnels')
async def _tunnel():
    pairs = {k: cache[k] for k in cache.keys() if k.startswith('tunnel')}
    return pairs


def pubmessage(que: str, msg: str, url: str = None):
    p = AMQPPublisher(que, url)
    p.publish(json.dumps(msg).encode('utf-8'))


@app.post('/amqp')
@app.get('/amqp')
async def post_amqp(info: Request):
    try:
        info = await info.json()
        queue_name = info['queue_name']
        message = info['message']
        url = info.get('url')
        resp = await async_render(pubmessage, queue_name, message, url)
        return {"result": "success", 'resp': str(resp)}
    except Exception as e:
        return {"result": "fail", "msg": str(e)}


@app.post('/shorten')
async def url_shorter(info: Request):
    req_info = await info.json()
    url = req_info.get('url')
    if not url.startswith('http'):
        url = 'http://' + url
    md5 = hashlib.md5(url.encode()).hexdigest()
    uniq_id = Hashids(salt=md5, min_length=6).encode(42)
    cf.info('uniq_id: ' + uniq_id)
    cache[uniq_id] = url
    cf.info('uniq id inserted')
    return {'code': 200, 'status': 'SUCCESS', 'url': 'http://localhost:9000/s/' + uniq_id}


@app.get('/s/{uniq_id}')
@app.post('/s/{uniq_id}')
async def decode_url(uniq_id: str):
    cf.info(uniq_id)
    cf.info(cache.get(uniq_id))
    url = cache.get(uniq_id) or 'https://www.baidu.com'
    return RedirectResponse(url)


@app.get('/fastbark/{title}/{message}')
@app.post('/fastbark/{title}/{message}')
async def bark_(title: str, message: str):
    url = (f"{auth.local_bark}/{title}/{message}?icon="
           "https://pbs.twimg.com/media/FmVlgF8WIAEbQvy?format=jpg")
    async with SingletonSession() as session:
        async with session.post(url) as resp:
            return await resp.json()


@app.post('/bark')
async def bark_(info: Request):
    info = await info.json()
    token = info['token']
    title = info['title']
    message = info['message']
    icon = info.get('icon')

    if token != auth.api_token:
        return {'code': 500, 'message': 'token error'}

    url = f"{auth.local_bark}/{title}/{message}"
    if icon:
        url = f"{url}?icon={icon}"
    async with SingletonSession() as session:
        async with session.post(url) as resp:
            return await resp.json()


async def bitly_helper(url: str) -> str:
    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    try:
        async with SingletonSession() as session:
            async with session.get(endpoint,
                                   params={
                                       'access_token': auth.bitlytoken,
                                       'longUrl': url
                                   }) as resp:
                r = await resp.json()
                return r['data']['url']
    except Exception as e:
        return {"error": str(e)}


@app.post('/bitly')
async def _bitly(info: Request) -> str:
    info = await info.json()
    url = info['url']
    if not url.startswith('http'):
        url = 'http://' + url
    return await bitly_helper(url)


@app.post('/humidifier/{action}')
async def _humidifier(action: str):
    db_url = auth.db_url
    async with SingletonSession() as session:
        async with session.post(db_url,
                                json={
                                    'key': 'humidifier',
                                    'value': action
                                }) as resp:
            _ = await resp.json()

        return {'action': action}


# --------------------------------------------------- Telegram


async def telegram_helper(channel: str, message: str) -> dict:
    bot = auth.telegram_bot
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id=@{}&text={}'.format(
        bot, channel, message)
    async with SingletonSession() as session:
        async with session.post(url) as resp:
            return await resp.json()


@app.post('/telegram')
async def _telegram(info: Request):
    info = await info.json()
    if 'message' not in info or 'channel' not in info:
        return {'code': 500, 'message': 'Please provide message and channel.'}
    return await telegram_helper(info['channel'], info['message'])


# --------------------------------------------------- IMs
@app.post('/mstdn/dlRCKPnV3wh9fmBOMW92VPu745Luiudm')
async def _mstdn(info: Request):
    info = await info.json()
    text = info['text']
    media = info.get('media', [])
    return await async_render(post_status, text, media)


@app.post('/tweet/yq1uzEhBQZpKH5JAN1w444h44KXayNd7')
async def _tweet(info: Request):
    info = await info.json()
    text = info['text']
    media = info.get('media', [])
    return await async_render(tweet_status, text, media)


# --------------------------------------------------- Auth


class AuthCache(object):
    host = None


@app.post('/auth')
async def _auth(info: Request) -> Union[str, List[str]]:
    """ For authentification. """
    info = await info.json()
    try:
        AuthCache.host = info['host']
        keys_list = info.get('keys', [])
        keys_str = ','.join(keys_list)
        hostname = info['hostname']
    except KeyError as e:
        return {'code': 500, 'message': str(e)}

    path = secrets.token_hex(16)
    auth_url = await bitly_helper(f'{AuthCache.host}/authhelper/{path}_{path}')
    payload = {
        'channel':
        'cowbark',
        'message': (f'Hostname: {hostname}%0A'
                    f'Keys to be authenticated: {keys_str} %0A %0A'
                    f'Confirm url: {auth_url}')
    }
    cf.info('payload: ' + str(payload))

    await telegram_helper(payload['channel'], payload['message'])
    async with aioredis.from_url('redis://localhost') as rd:
        for _ in range(60):
            v = await rd.get(path)
            if v:
                return {'values': [auth.get(k) for k in keys_list]}
            await asyncio.sleep(1)

    return {
        'code': 500,
        'status': 'Auth failed',
        'values': [None] * len(keys_list)
    }


def generate_html_response(path: str):
    html_content = f"""
    <html>
        <head>
            <style>
            div {{  
                border: 3px solid gray;  
                padding: 100px;  
                background-color: orange;  
                text-align: center;
                border-radius: 25px;
                font-size: 40px;
                }}  
            </style>
            <title>Auth</title>
        </head>
        <body>
        <div> <a href="{path}">Click here to confirm auth.</a> </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/authhelper/{path}')
async def _authhelper(path: str, response_class=HTMLResponse):
    async with aioredis.from_url('redis://localhost') as redis:
        is_exist = await redis.exists(path)
        await redis.setex(path, 86400, 1)
        if '_' in path:
            path_new = path.split('_')[0]
            return generate_html_response(
                f'{AuthCache.host}/authhelper/{path_new}')
        else:
            if is_exist:
                return {'code': 303, 'status': 'ALREADY AUTHED', 'path': path}
            return {'code': 200, 'status': 'AUTH SUCCESS', 'path': path}


@app.post('/image')
async def _imagehosting(file: UploadFile = File(...)):
    """ A simple image hosting based on github repo."""
    try:
        content = await file.read()
        md5 = hashlib.md5(content).hexdigest()
        async with aioredis.from_url('redis://localhost') as rd:
            if await rd.exists(md5):
                return {
                    'code': 200,
                    'status': 'ALREADY EXISTS',
                    'url': await rd.get(md5)
                }
            else:
                url = await github_upload(content)
                await rd.setex(md5, 86400 * 30, url)
                return {'code': 200, 'status': 'UPLOAD SUCCESS', 'url': url}
    except Exception as e:
        return {
            'code': 500,
            'status': 'UPLOAD FAILED',
            'message': str(e),
            'url': None
        }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
