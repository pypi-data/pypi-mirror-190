#!/usr/bin/env python3
import asyncio
from pyserverless.bases import bitly_helper
import base64
import hashlib
import os
from datetime import datetime
from typing import Tuple

from codefast.asyncio import async_render

from pyserverless.auth import auth

try:
    os.system('pip3 install PyGithub')
    os.system('pip3 install python-multipart')
except:
    pass


def get_year_month() -> Tuple[str, str]:
    today = datetime.today()
    return today.year, today.month, today.day


def get_info(content: bytes) -> 'Info':
    data = base64.b64encode(content)
    file_name = hashlib.md5(content).hexdigest() + '.png'

    year, month, day = get_year_month()
    path = f'{year}/{month}/{day}/{file_name}'
    return type('Info', (object,), {'data': data, 'file_name': file_name, 'path': path})


def _github_upload(_token: str, data: str, file_name: str, path: str) -> str:
    from github import Github, InputGitTreeElement
    repo = Github(_token, timeout=300).get_user().get_repo('imagehosting')
    blob = repo.create_git_blob(data.decode("utf-8"), "base64")
    element = InputGitTreeElement(path=path,
                                  mode='100644',
                                  type='blob',
                                  sha=blob.sha)
    element_list = list()
    element_list.append(element)

    blob = repo.create_git_blob(data.decode("utf-8"), "base64")
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(f"doc(2023): uploading {file_name }", tree, [parent])
    master_ref.edit(commit.sha)
    return True


async def get_url(path: str) -> str:
    return await bitly_helper(path)


async def parallel(content: bytes) -> str:
    token = auth['117_git_token']
    info = get_info(content)
    path = f'https://cdn.jsdelivr.net/gh/117v2/imagehosting/{info.path}'
    await async_render(_github_upload, token, info.data, info.file_name, info.path)
    return await get_url(path)


async def github_upload(content: bytes) -> str:
    return await parallel(content)
