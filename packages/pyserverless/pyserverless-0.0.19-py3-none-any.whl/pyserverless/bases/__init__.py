#!/usr/bin/env python3

import codefast as cf

import aiohttp

from pyserverless.auth import auth


class SingletonSession(object):
    uniq_instance = {}

    def __new__(cls, *args, **kwargs):
        if not args:
            args = ('__main__', )
        if cls.uniq_instance.get(id(args[0])) is None:
            cls.uniq_instance[id(args[0])] = super().__new__(cls)
            cls.uniq_instance[id(args[0])].session = aiohttp.ClientSession()
        return cls.uniq_instance[id(args[0])]

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


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
